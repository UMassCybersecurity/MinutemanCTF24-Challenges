main:
        pushq   %rbp
        pushq   %rbx
        subq    $8, %rsp
        movl    $0, %ebx
        movl    $-1919252018, %ebp
        jmp     .L2
.L3:
        movl    %ebp, %edi
        notl    %edi
        movzbl  %dil, %edi
        movq    $1, %rsi  // what's a calling convention
        call    putc // look at man page for putc
        shrl    $8, %ebp
        addl    $1, %ebx
.L2:
        cmpl    $3, %ebx
        jle     .L3
        movl    $0, %eax
        addq    $8, %rsp
        popq    %rbx
        popq    %rbp
        ret