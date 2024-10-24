.intel_syntax noprefix;

check_activation_code:
        mov     ecx, 0
        mov     eax, 0
        mov     r8d, -561407347
        mov     esi, -1987406954
        jmp     .L2
.L3:
        mov     edx, esi
        xor     dl, BYTE PTR [rdi+rcx]
        not     dl
        add     rax, rdx
        mov     edx, r8d
        xor     dl, BYTE PTR [rdi+4+rcx]
        not     dl
        add     rax, rdx
        shr     esi, 8
        shr     r8d, 8
        add     rcx, 1
.L2:
        cmp     rcx, 3
        jle     .L3
        ret
.LC0:
        .string "enter the activation code:"
.LC1:
        .string "%8s"
.LC2:
        .string "Wrong activation code!"
.LC3:
        .string ""
main:
        push    rbx
        sub     rsp, 16
        mov     QWORD PTR [rsp+8], 0
        mov     edi, OFFSET FLAT:.LC0
        call    puts
        lea     rbx, [rsp+8]
        mov     rsi, rbx
        mov     edi, OFFSET FLAT:.LC1
        mov     eax, 0
        call    __isoc99_scanf
        mov     rdi, rbx
        call    check_activation_code
        mov     ebx, eax
        test    al, al
        je      .L5
        mov     edi, OFFSET FLAT:.LC2
        call    puts
        movsx   eax, bl
        jmp     .L4
.L7:
        movsx   ecx, bl
        movsx   rdx, bl
        mov     eax, 7
        sub     eax, ecx
        cdqe
        movzx   edi, BYTE PTR [rsp+8+rax]
        xor     dil, BYTE PTR trinity[rdx]
        movsx   edi, dil
        mov     rsi, QWORD PTR stdout[rip]
        call    putc
        add     ebx, 1
.L5:
        cmp     bl, 7
        jle     .L7
        mov     edi, OFFSET FLAT:.LC3
        call    puts
        mov     eax, 0
.L4:
        add     rsp, 16
        pop     rbx
        ret
trinity:
        .ascii  "\020\002\022B\004\036_\r"