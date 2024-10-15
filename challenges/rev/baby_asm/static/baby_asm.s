baby:
    push    rbp
    mov     rbp, rsp
    mov     dword ptr [rbp - 4], edi
    mov     eax, dword ptr [rbp - 4]
    mov     ecx, dword ptr [rbp - 4]
    imul    rax, rcx
    mov     qword ptr [rbp - 16], rax
    mov     rax, qword ptr [rbp - 16]
    add     rax, 1122488755
    mov     qword ptr [rbp - 16], rax
    mov     rax, qword ptr [rbp - 16]
    pop     rbp
    ret
