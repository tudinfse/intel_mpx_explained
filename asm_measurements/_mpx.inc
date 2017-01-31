;----------------------------------------------------------------------------
;                       mpx.inc                  2016-08-08 Oleksii Oleksenko
;
;            PMC Test program for MPX instructions
; The following macros can be defined on the command line or in include files:
;
; instruct:     The name of a single instruction to test
;
; regsize:      Register size: 8, 16, 32, 64, 128, 256, (or 65 = mmx)
;
; numop:        Number of operands: 1, 2 or 3
;
; tmode:        L:  Latency with memory operand
;               M:  Throughput with memory operand
;-----------------------------------------------------------------------------
; Define any undefined macros

%ifndef tmode
   %define tmode  L          ; default: measure latency
%endif

%ifndef regsize              ; default: define registers as 32 bit
   %define regsize   64
%endif

%ifndef argmode
   %define argmode  bm          ; default: check memory
%endif



;##############################################################################
;#
;#                 Test code macro
;#
;##############################################################################


; main testcode macro
%macro testcode 0
BITS 64

        mov rbp,1000

; initialize the bounds registers for further checks
        mov   rax,  0x3
        mov   rcx,  rsi

        bndmk bnd0, [rsi+rax]
        add   rsi,  regsize
        bndmk bnd1, [rsi+rax]
        add   rsi,  regsize
        bndmk bnd2, [rsi+rax]
        add   rsi,  regsize
        bndmk bnd3, [rsi+rax]

        mov   rsi,  rcx

Testloop1:


; ================== bm ================
%IFIDNI argmode, bm

    %IFIDNI tmode, L         ; measure latency, 2 operands

       %rep 100
            instruct bnd0, [rsi]
       %endrep

    %ELIFIDNI tmode, M         ; measure throughput with 2 operands, including 1 memory operand

       %rep 25
            instruct bnd0, [rsi]
            instruct bnd1, [rsi+regsize]
            instruct bnd2, [rsi+regsize*2]
            instruct bnd3, [rsi+regsize*3]
       %endrep

    %ELSE
       %error unknown testmode
    %ENDIF

; ================== br ================
%ELIFIDNI argmode, br
    lea rax, [rsi]
    lea rbx, [rsi+regsize]
    lea rcx, [rsi+regsize*2]
    lea rdx, [rsi+regsize*3]

    %IFIDNI tmode, L         ; measure latency, 2 operands

       %rep 100
            instruct bnd0, rax
       %endrep

    %ELIFIDNI tmode, M         ; measure throughput with 2 operands, including 1 memory operand

       %rep 25
            instruct bnd0, rax
            instruct bnd1, rbx
            instruct bnd2, rcx
            instruct bnd3, rdx
       %endrep

    %ELSE
       %error unknown testmode
    %ENDIF

; ================== bb ================
%ELIFIDNI argmode, bb

    %IFIDNI tmode, L         ; measure latency, 2 operands

       %rep 50
            instruct bnd0, bnd1
            instruct bnd1, bnd0
       %endrep

    %ELIFIDNI tmode, M         ; measure throughput with 2 operands, including 1 memory operand

       %rep 25
            instruct bnd1, bnd0
            instruct bnd2, bnd0
            instruct bnd3, bnd0
            instruct bnd0, bnd0
       %endrep

    %ELSE
       %error unknown testmode
    %ENDIF

; ================== mb ================
%ELIFIDNI argmode, mb

    %IFIDNI tmode, L         ; measure latency, 2 operands

       %rep 100
            instruct [rsi], bnd0
       %endrep

    %ELIFIDNI tmode, M         ; measure throughput with 2 operands, including 1 memory operand

       %rep 25
            instruct [rsi], bnd0
            instruct [rsi+regsize], bnd1
            instruct [rsi+regsize*2], bnd2
            instruct [rsi+regsize*3], bnd3
       %endrep

    %ELSE
       %error unknown testmode
    %ENDIF

; ================= unknown ==============
%ELSE
   %error unknown instruction
%ENDIF
        dec rbp
        jnz Testloop1
%endmacro

; disable default test loops
%define repeat1 1
%define repeat2 1

