baby:
    push    rbp
    mov     rbp, rsp
    mov     dword ptr [rbp - 4], edi
    mov     eax, dword ptr [rbp - 4]
    imul    eax, dword ptr [rbp - 4]
    mov     dword ptr [rbp - 4], eax
    mov     eax, dword ptr [rbp - 4]
    add     eax, 1122488755
    mov     dword ptr [rbp - 4], eax
    mov     eax, dword ptr [rbp - 4]
    pop     rbp
    ret
