.globl check_activation_code
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