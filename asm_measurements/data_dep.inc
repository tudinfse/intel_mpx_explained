;----------------------------------------------------------------------------
;                       mpx.inc                  2016-08-08 Oleksii Oleksenko
;
;            PMC Test program for MPX instructions
; The following macros can be defined on the command line or in include files:
;
; instruct:     The name of a single instruction to test
;
; type:        simple:  only load/store
;              check:  only bounds check
;              cc: two checks
;              ca: check one bound and access memory
;              cca: check both bounds and access memory
;              rcca: check both bounds in reverted order and access memory
;
; argmode      load_direct: load from memory (direct address)
;              store_direct: store to memory (direct address)
;              load_relative: load from memory (relative address)
;              store_relative: store to memory (relative address)
;-----------------------------------------------------------------------------
; Define any undefined macros

%ifndef type
   %define type  s          ; default: simple
%endif

%ifndef argmode
   %define argmode  l          ; default: load
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
        mov rdx, 40
        lea r8, [rsi]

; initialize the bounds registers for further checks
        mov   rax,  0x5
        mov   rcx,  rsi
        mov   r9,   0x2

        bndmk bnd0, [rsi+rax]
        add   rsi,  regsize
        bndmk bnd1, [rsi+rax]
        add   rsi,  regsize
        bndmk bnd2, [rsi+rax]
        add   rsi,  regsize
        bndmk bnd3, [rsi+rax]

        mov   rsi,  rcx

; used registers: rax, rcx, rdx rsi, rbp
; rbx - reserved for loading into it

Testloop1:


; ================== simple ================
%IFIDNI type, s

    %IFIDNI argmode, load_direct  ; load

       %rep 100
            mov rbx, [r8]
       %endrep

    %ELIFIDNI argmode, store_direct  ; store

       %rep 100
            mov [r8], rdx
       %endrep

    %ELIFIDNI argmode, load_relative  ; load

       %rep 100
            mov rbx, [r8+r9]
       %endrep

    %ELIFIDNI argmode, store_relative  ; store

       %rep 100
            mov [r8+r9], rdx
       %endrep

    %ELSE
       %error unknown argmode
    %ENDIF

; ================== check ================
%ELIFIDNI type, c

    %IFIDNI argmode, load_direct  ; load

        %rep 100
            instruct bnd0, r8
        %endrep

    %ELIFIDNI argmode, load_relative  ; store

        %rep 100
            instruct bnd0, [r8+r9]
        %endrep

    %ELSE
       %error unknown argmode
    %ENDIF


; ================== both checks ================
%ELIFIDNI type, cc

    %IFIDNI argmode, load_direct  ; load

        %rep 100
            bndcl bnd0, r8
            bndcu bnd0, r8
        %endrep

    %ELIFIDNI argmode, load_relative  ; store

        %rep 100
            bndcl bnd0, [r8+r9]
            bndcu bnd0, [r8+r9+1]
        %endrep

    %ELSE
       %error unknown argmode
    %ENDIF

; ================== check and access ================
%ELIFIDNI type, ca

    %IFIDNI argmode, load_direct  ; load

        %rep 100
            instruct bnd0, r8
            mov rbx, [r8]
        %endrep

    %ELIFIDNI argmode, store_direct  ; store

        %rep 100
            instruct bnd0, r8
            mov [r8], rdx
        %endrep

    %ELIFIDNI argmode, load_relative  ; load

        %rep 100
            instruct bnd0, [r8+r9]
            mov rbx, [r8+r9]
        %endrep

    %ELIFIDNI argmode, store_relative  ; store

        %rep 100
            instruct bnd0, [r8+r9]
            mov [r8+r9], rdx
        %endrep

    %ELSE
       %error unknown argmode
    %ENDIF

; ================== two checks and access ================
%ELIFIDNI type, cca

    %IFIDNI argmode, load_direct  ; load

        %rep 100
            bndcl bnd0, r8
            bndcu bnd0, r8
            mov rbx, [r8]
        %endrep

    %ELIFIDNI argmode, store_direct  ; store

        %rep 100
            bndcl bnd0, r8
            bndcu bnd0, r8
            mov [r8], rdx
        %endrep

    %ELIFIDNI argmode, load_relative  ; load

        %rep 100
            bndcl bnd0, [r8+r9]
            bndcu bnd0, [r8+r9+1]
            mov rbx, [r8+r9]
        %endrep

    %ELIFIDNI argmode, store_relative  ; store

        %rep 100
            bndcl bnd0, [r8+r9]
            bndcu bnd0, [r8+r9+1]
            mov [r8+r9], rdx
        %endrep

    %ELSE
       %error unknown argmode
    %ENDIF

; ================== two checks (reverted) and access ================
%ELIFIDNI type, rcca

    %IFIDNI argmode, load_direct  ; load

        %rep 100
            bndcu bnd0, r8
            bndcl bnd0, r8
            mov rbx, [r8]
        %endrep

    %ELIFIDNI argmode, store_direct  ; store

        %rep 100
            bndcu bnd0, r8
            bndcl bnd0, r8
            mov [r8], rdx
        %endrep

    %ELIFIDNI argmode, load_relative  ; load

        %rep 100
            bndcu bnd0, [r8+r9+1]
            bndcl bnd0, [r8+r9]
            mov rbx, [r8+r9]
        %endrep

    %ELIFIDNI argmode, store_relative  ; store

        %rep 100
            bndcu bnd0, [r8+r9+1]
            bndcl bnd0, [r8+r9]
            mov [r8+r9], rdx
        %endrep

    %ELSE
       %error unknown argmode
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

