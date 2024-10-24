.LC0:
        .string "enter the activation code:"
.LC1:
        .string "%8s"
.LC2:
        .string ""
main:
        pushq   %rbp
        movl    $.LC0, %edi
        pushq   %rbx
        xorl    %ebx, %ebx
        subq    $24, %rsp
        andq    $0, 8(%rsp)
        leaq    15(%rsp), %rbp
        call    puts
        leaq    8(%rsp), %rsi
        movl    $.LC1, %edi
        xorl    %eax, %eax
        call    __isoc99_scanf
.L2:
        movq    %rbp, %rax
        subq    %rbx, %rax
        incq    %rbx
        movb    (%rax), %dil
        xorb    trinity-1(%rbx), %dil
        movsbl  %dil, %edi
        call    putchar
        cmpq    $8, %rbx
        jne     .L2
        movl    $.LC2, %edi
        call    puts
        addq    $24, %rsp
        xorl    %eax, %eax
        popq    %rbx
        popq    %rbp
        ret
trinity:
        .ascii  "\020\002\022B\004\036_\r"