main:
        push    {r3, r4, r5, lr}
        movs    r4, #0
        ldr     r5, .L5
        b       .L2
.L3:
        mvns    r0, r5
        ldr     r3, .L5+4
        ldr     r1, [r3]
        and     r0, r0, #255
        bl      putc
        lsrs    r5, r5, #8
        adds    r4, r4, #1
.L2:
        cmp     r4, #3
        ble     .L3
        movs    r0, #0
        pop     {r3, r4, r5, pc}
.L5:
        .word   -1919252018
        .word   stdout