check_activation_code:
        movl    $0, %ecx
        movl    $0, %eax
        movl    $-561407347, %r8d
        movl    $-1987406954, %esi
        jmp     .L2
.L3:
        movl    %esi, %edx
        xorb    (%rdi,%rcx), %dl
        notl    %dl
        addq    %rdx, %rax
        movl    %r8d, %edx
        xorb    4(%rdi,%rcx), %dl
        notl    %dl
        addq    %rdx, %rax
        shrl    $8, %esi
        shrl    $8, %r8d
        addq    $1, %rcx
.L2:
        cmpq    $3, %rcx
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
        pushq   %rbx
        subq    $16, %rsp
        movq    $0, 8(%rsp)
        movl    $.LC0, %edi
        call    puts
        leaq    8(%rsp), %rbx
        movq    %rbx, %rsi
        movl    $.LC1, %edi
        movl    $0, %eax
        call    __isoc99_scanf
        movq    %rbx, %rdi
        call    check_activation_code
        movl    %eax, %ebx
        testb   %al, %al
        je      .L5
        movl    $.LC2, %edi
        call    puts
        movsbl  %bl, %eax
        jmp     .L4
.L7:
        movsbl  %bl, %ecx
        movsbq  %bl, %rdx
        movl    $7, %eax
        subl    %ecx, %eax
        cltq
        movzbl  8(%rsp,%rax), %edi
        xorb    trinity(%rdx), %dil
        movsbl  %dil, %edi
        movq    stdout(%rip), %rsi
        call    putc
        addl    $1, %ebx
.L5:
        cmpb    $7, %bl
        jle     .L7
        movl    $.LC3, %edi
        call    puts
        movl    $0, %eax
.L4:
        addq    $16, %rsp
        popq    %rbx
        ret
trinity:
        .ascii  "\020\002\022B\004\036_\r"