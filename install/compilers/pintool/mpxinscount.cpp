#include "pin.H"
#include <iostream>
#include <fstream>
extern "C" {
#include "xed-interface.h"
}

KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE,  "pintool",
    "o", "", "specify file name for MyPinTool output");

//KNOB<BOOL> knob_mpx_mode(KNOB_MODE_WRITEONCE,"supported:xed","xed_mpx_mode","1","Enable Intel(R) MPX instruction decoding");

std::ostream * out = &cerr;
PIN_LOCK lock;

INT32 numThreads = 0;
const INT32 MaxNumThreads = 10000;

struct THREAD_DATA
{
    //// first 8 UINT64 members
    UINT64 _total;
    UINT64 _memreads;
    UINT64 _memwrites;
    UINT64 _bndmk;    // making bounds (# of pointers instrumented)
    UINT64 _bndcl;    // lower bound check
    UINT64 _bndcu;    // +bndcn, upper bound check
    UINT64 _bndldx;   // bounds load from BD & BT
    UINT64 _bndstx;   // bounds store to BD & BT
    //// second 8 UINT64 members
    UINT64 _bndmovreg;   // bounds register move (reg-reg only)
    UINT64 _bndmovmem;   // bounds register move (mem-reg, reg-mem)
    UINT8 _pad[6*8];  // (assume 64-byte cache line)
};

THREAD_DATA icount[MaxNumThreads];


/* ===================================================================== */
/* Analysis component (must be fast and inlinable)                       */
/* ===================================================================== */
typedef VOID (*countfun_t)(THREADID);

VOID countTotal(THREADID tid) {
    icount[tid]._total++;
}

VOID countMemRead(THREADID tid) {
    icount[tid]._memreads++;
}

VOID countMemWrite(THREADID tid) {
    icount[tid]._memwrites++;
}

VOID countBndmk(THREADID tid) {
    icount[tid]._bndmk++;
}

VOID countBndcl(THREADID tid) {
    icount[tid]._bndcl++;
}

VOID countBndcu(THREADID tid) {
    icount[tid]._bndcu++;
}

VOID countBndldx(THREADID tid) {
    icount[tid]._bndldx++;
}

VOID countBndstx(THREADID tid) {
    icount[tid]._bndstx++;
}

VOID countBndmovReg(THREADID tid) {
    icount[tid]._bndmovreg++;
}

VOID countBndmovMem(THREADID tid) {
    icount[tid]._bndmovmem++;
}

countfun_t chooseCountFun(xed_iclass_enum_t iclass, UINT32 memOperands) {
    switch (iclass) {
        case XED_ICLASS_BNDMK:   return countBndmk;
        case XED_ICLASS_BNDCL:   return countBndcl;
        // do not distinguish between normal and one-complement versions of ins
        case XED_ICLASS_BNDCN:
        case XED_ICLASS_BNDCU:   return countBndcu;
        case XED_ICLASS_BNDLDX:  return countBndldx;
        case XED_ICLASS_BNDSTX:  return countBndstx;
        case XED_ICLASS_BNDMOV:  return (memOperands <= 0 ? countBndmovReg : countBndmovMem);
        default:                 return NULL;
    }
    return NULL;
}

VOID use_xed(THREADID tid, ADDRINT pc) {
    // [ taken from xed-print.cpp ]
#if defined(TARGET_IA32E)
    static const xed_state_t dstate = {XED_MACHINE_MODE_LONG_64, XED_ADDRESS_WIDTH_64b};
#else
    static const xed_state_t dstate = { XED_MACHINE_MODE_LEGACY_32, XED_ADDRESS_WIDTH_32b};
#endif
    xed_decoded_inst_t xedd;
    xed_decoded_inst_zero_set_mode(&xedd, &dstate);
    xed3_operand_set_mpxmode(&xedd, 1);

    //Pass in the proper length: 15 is the max. But if you do not want to
    //cross pages, you can pass less than 15 bytes, of course, the
    //instruction might not decode if not enough bytes are provided.
    const unsigned int max_inst_len = 15;

    xed_error_enum_t xed_code = xed_decode(&xedd, reinterpret_cast<UINT8*>(pc), max_inst_len);
    BOOL xed_ok = (xed_code == XED_ERROR_NONE);
    if (xed_ok) {
        xed_iclass_enum_t iclass = xed_decoded_inst_get_iclass(&xedd);
        xed_uint_t memOperands = xed_decoded_inst_number_of_memory_operands(&xedd);
        countfun_t countFun = chooseCountFun(iclass, memOperands);
        if (countFun)
            countFun(tid);
    }

}


/* ===================================================================== */
/* Instrumentation component                                             */
/* ===================================================================== */
VOID Instruction(INS ins, VOID *v) {
    // in general, we use InsertPredicatedCall to count *really executed* ins
    INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)countTotal, IARG_THREAD_ID, IARG_END);

    UINT32 memOperands = INS_MemoryOperandCount(ins);
    for (UINT32 memOp = 0; memOp < memOperands; memOp++) {
        if (INS_MemoryOperandIsRead(ins, memOp)) {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)countMemRead,
                IARG_THREAD_ID,
                IARG_END);
        }
        if (INS_MemoryOperandIsWritten(ins, memOp)) {
            INS_InsertPredicatedCall(
                ins, IPOINT_BEFORE, (AFUNPTR)countMemWrite,
                IARG_THREAD_ID,
                IARG_END);
        }
    }

    xed_iclass_enum_t iclass = (xed_iclass_enum_t)INS_Opcode(ins);
    countfun_t countFun = chooseCountFun(iclass, memOperands);

    if (countFun) {
        INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)countFun, IARG_THREAD_ID, IARG_END);
    } else {
        // work-around bug of INS_Opcode considering MPX ins as NOPs (we decode ins ourselves)
        switch (iclass) {
            case XED_ICLASS_NOP:
            case XED_ICLASS_NOP2:
            case XED_ICLASS_NOP3:
            case XED_ICLASS_NOP4:
            case XED_ICLASS_NOP5:
            case XED_ICLASS_NOP6:
            case XED_ICLASS_NOP7:
            case XED_ICLASS_NOP8:
            case XED_ICLASS_NOP9:
            case XED_ICLASS_FNOP:
                INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)use_xed, IARG_THREAD_ID, IARG_INST_PTR, IARG_END);
            default:
                break; // do nothing
        }
    }
}

/* ===================================================================== */
/* Output                                                                */
/* ===================================================================== */
VOID Fini(INT32 code, VOID *v)
{
    *out << "[mpxinscount] Number of threads ever exist = " << numThreads << endl;
    *out << "-----------------------------------------------" << endl;

    UINT64 total     = 0;
    UINT64 memreads  = 0;
    UINT64 memwrites = 0;
    UINT64 bndmk     = 0;
    UINT64 bndcl     = 0;
    UINT64 bndcu     = 0;
    UINT64 bndldx    = 0;
    UINT64 bndstx    = 0;
    UINT64 bndmovreg = 0;
    UINT64 bndmovmem = 0;

    for (INT32 t=0; t<numThreads; t++) {
        *out << "thread\t" << decstr(t) << ": total     = " << icount[t]._total << endl;
        *out << "thread\t" << decstr(t) << ": memreads  = " << icount[t]._memreads << endl;
        *out << "thread\t" << decstr(t) << ": memwrites = " << icount[t]._memwrites << endl;
        *out << "thread\t" << decstr(t) << ": bndmk     = " << icount[t]._bndmk << endl;
        *out << "thread\t" << decstr(t) << ": bndcl     = " << icount[t]._bndcl << endl;
        *out << "thread\t" << decstr(t) << ": bndcu     = " << icount[t]._bndcu << endl;
        *out << "thread\t" << decstr(t) << ": bndldx    = " << icount[t]._bndldx << endl;
        *out << "thread\t" << decstr(t) << ": bndstx    = " << icount[t]._bndstx << endl;
        *out << "thread\t" << decstr(t) << ": bndmovreg = " << icount[t]._bndmovreg << endl;
        *out << "thread\t" << decstr(t) << ": bndmovmem = " << icount[t]._bndmovmem << endl;
        *out << endl;

        total     += icount[t]._total;
        memreads  += icount[t]._memreads;
        memwrites += icount[t]._memwrites;
        bndmk     += icount[t]._bndmk;
        bndcl     += icount[t]._bndcl;
        bndcu     += icount[t]._bndcu;
        bndldx    += icount[t]._bndldx;
        bndstx    += icount[t]._bndstx;
        bndmovreg += icount[t]._bndmovreg;
        bndmovmem += icount[t]._bndmovmem;
    }

    *out << "-----------------------------------------------" << endl;
    *out << "program: total     = " << total << endl;
    *out << "program: memreads  = " << memreads << endl;
    *out << "program: memwrites = " << memwrites << endl;
    *out << "program: bndmk     = " << bndmk << endl;
    *out << "program: bndcl     = " << bndcl << endl;
    *out << "program: bndcu     = " << bndcu << endl;
    *out << "program: bndldx    = " << bndldx << endl;
    *out << "program: bndstx    = " << bndstx << endl;
    *out << "program: bndmovreg = " << bndmovreg << endl;
    *out << "program: bndmovmem = " << bndmovmem << endl;
}

/* ===================================================================== */
/* Helpers                                                               */
/* ===================================================================== */
INT32 Usage()
{
    cerr << "This Pintool counts the number of MPX instructions executed" << endl;
    cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}

VOID ThreadStart(THREADID threadid, CONTEXT *ctxt, INT32 flags, VOID *v)
{
    PIN_GetLock(&lock, threadid+1);
    numThreads++;
    PIN_ReleaseLock(&lock);
    ASSERT(numThreads <= MaxNumThreads, "Maximum number of threads exceeded\n");
}


/* ===================================================================== */
/* Main                                                                  */
/* ===================================================================== */
int main(int argc, char * argv[])
{
    // Initialize pin
    if (PIN_Init(argc, argv)) return Usage();

    string fileName = KnobOutputFile.Value();
    if (!fileName.empty()) { out = new std::ofstream(fileName.c_str());}

    // Initialize icount[]
    for (INT32 t=0; t<MaxNumThreads; t++)
        memset(&icount[t], 0, sizeof(THREAD_DATA));

    PIN_InitLock(&lock);
    PIN_AddThreadStartFunction(ThreadStart, 0);

    // Register Instruction to be called to instrument instructions
    INS_AddInstrumentFunction(Instruction, 0);

    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Fini, 0);

    // Start the program, never returns
    PIN_StartProgram();

    return 0;
}
