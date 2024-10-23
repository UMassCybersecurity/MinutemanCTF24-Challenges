.LC0:
        .string "enter the activation code:"
.LC1:
        .string "%8s"
.LC2:
        .string ""
main:
        push    rbp
        mov     edi, OFFSET FLAT:.LC0
        push    rbx
        xor     ebx, ebx
        sub     rsp, 24
        and     QWORD PTR [rsp+8], 0
        lea     rbp, [rsp+15]
        call    puts
        lea     rsi, [rsp+8]
        mov     edi, OFFSET FLAT:.LC1
        xor     eax, eax
        call    __isoc99_scanf
.L2:
        mov     rax, rbp
        sub     rax, rbx
        inc     rbx
        mov     dil, BYTE PTR [rax]
        xor     dil, BYTE PTR trinity[rbx-1]
        movsx   edi, dil
        call    putchar
        cmp     rbx, 8
        jne     .L2
        mov     edi, OFFSET FLAT:.LC2
        call    puts
        add     rsp, 24
        xor     eax, eax
        pop     rbx
        pop     rbp
        ret
trinity:
        .ascii  "\020\002\022B\004\036_\r"