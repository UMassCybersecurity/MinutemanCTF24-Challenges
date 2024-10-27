check_activation_code:
        push    {r4, lr}
        mov     ip, r0
        movs    r3, #0
        mov     r0, r3
        ldr     r4, .L5
        ldr     r1, .L5+4
        b       .L2
.L3:
        ldrb    r2, [ip, r3]    @ zero_extendqisi2
        uxtb    lr, r1
        eor     r2, r2, lr
        subs    r0, r0, r2
        subs    r0, r0, #1
        add     r2, ip, r3
        ldrb    r2, [r2, #4]    @ zero_extendqisi2
        uxtb    lr, r4
        eor     r2, r2, lr
        subs    r0, r0, r2
        subs    r0, r0, #1
        lsrs    r1, r1, #8
        lsrs    r4, r4, #8
        adds    r3, r3, #1
.L2:
        cmp     r3, #3
        ble     .L3
        pop     {r4, pc}
.L5:
        .word   -561407347
        .word   -1987406954
.LC0:
        .ascii  "enter the activation code:\000"
.LC1:
        .ascii  "%8s\000"
.LC2:
        .ascii  "Wrong activation code!\000"
.LC3:
        .ascii  "\000"
main:
        push    {r4, r5, lr}
        sub     sp, sp, #12
        movs    r3, #0
        str     r3, [sp]
        str     r3, [sp, #4]
        ldr     r0, .L12
        bl      puts
        mov     r1, sp
        ldr     r0, .L12+4
        bl      __isoc99_scanf
        mov     r0, sp
        bl      check_activation_code
        ands    r4, r0, #255
        beq     .L8
        mov     r5, r0
        ldr     r0, .L12+8
        bl      puts
        uxtb    r0, r5
        b       .L7
.L10:
        ldr     r3, .L12+12
        ldrb    r0, [r3, r4]    @ zero_extendqisi2
        rsb     r3, r4, #7
        adds    r3, r3, #8
        add     r3, sp, r3
        ldrb    r3, [r3, #-8]   @ zero_extendqisi2
        ldr     r2, .L12+16
        ldr     r1, [r2]
        eors    r0, r0, r3
        bl      putc
        adds    r4, r4, #1
        uxtb    r4, r4
.L8:
        cmp     r4, #7
        bls     .L10
        ldr     r0, .L12+20
        bl      puts
        movs    r0, #0
.L7:
        add     sp, sp, #12
        pop     {r4, r5, pc}
.L12:
        .word   .LC0
        .word   .LC1
        .word   .LC2
        .word   .LANCHOR0
        .word   stdout
        .word   .LC3
trinity:
        .ascii  "\020\002\022B\004\036_\015"