baby:
        pushq   %rbp
        movq    %rsp, %rbp
        movl    %edi, -4(%rbp)
        movl    -4(%rbp), %eax
        movl    -4(%rbp), %ecx
        imulq   %rcx, %rax
        movq    %rax, -16(%rbp)
        movq    -16(%rbp), %rax
        addq    $1122488755, %rax
        movq    %rax, -16(%rbp)
        movq    -16(%rbp), %rax
        popq    %rbp
        retq
