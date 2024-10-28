main:
        push    rbp
        push    rbx
        sub     rsp, 8
        mov     ebx, 0
        mov     ebp, -1919252018
        jmp     .L2
.L3:
        mov     edi, ebp
        not     edi
        movzx   edi, dil
        mov     rsi, 1 // what's a calling convention
        call    putc // look at man page for putc
        shr     ebp, 8
        add     ebx, 1
.L2:
        cmp     ebx, 3
        jle     .L3
        mov     eax, 0
        add     rsp, 8
        pop     rbx
        pop     rbp
        ret