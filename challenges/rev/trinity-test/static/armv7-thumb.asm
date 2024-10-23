.LC0:
        .ascii  "enter the activation code:\000"
.LC1:
        .ascii  "%8s\000"
.LC2:
        .ascii  "\000"
main:
        push    {r0, r1, r4, r5, r6, lr}
        movs    r3, #0
        ldr     r0, .L4
        str     r3, [sp]
        str     r3, [sp, #4]
        bl      puts
        ldr     r0, .L4+4
        ldr     r6, .L4+8
        mov     r1, sp
        bl      __isoc99_scanf
        mov     r5, sp
        movs    r4, #7
.L2:
        ldrb    r3, [r5, r4]    @ zero_extendqisi2
        ldrb    r0, [r6], #1    @ zero_extendqisi2
        eors    r0, r0, r3
        bl      putchar
        subs    r4, r4, #1
        bcs     .L2
        ldr     r0, .L4+12
        bl      puts
        movs    r0, #0
        add     sp, sp, #8
        pop     {r4, r5, r6, pc}
.L4:
        .word   .LC0
        .word   .LC1
        .word   .LANCHOR0
        .word   .LC2
trinity:
        .ascii  "\020\002\022B\004\036_\015"