trinity:
        .ascii  "\020\002\022B\004\036_\r"
.LC0:
        .string "enter the activation code:"
.LC1:
        .string "%8s"
.LC2:
        .string ""
main:
        stp     x29, x30, [sp, -32]!
        mov     x29, sp
        str     xzr, [sp, 16]
        adrp    x0, .LC0
        add     x0, x0, :lo12:.LC0
        bl      puts
        add     x0, sp, 16
        mov     x1, x0
        adrp    x0, .LC1
        add     x0, x0, :lo12:.LC1
        bl      __isoc99_scanf
        str     wzr, [sp, 28]
        b       .L2
.L3:
        adrp    x0, trinity
        add     x1, x0, :lo12:trinity
        ldrsw   x0, [sp, 28]
        ldrb    w1, [x1, x0]
        mov     w2, 7
        ldr     w0, [sp, 28]
        sub     w0, w2, w0
        sxtw    x0, w0
        add     x2, sp, 16
        ldrb    w0, [x2, x0]
        eor     w0, w1, w0
        and     w0, w0, 255
        bl      putchar
        ldr     w0, [sp, 28]
        add     w0, w0, 1
        str     w0, [sp, 28]
.L2:
        ldr     w0, [sp, 28]
        cmp     w0, 7
        ble     .L3
        adrp    x0, .LC2
        add     x0, x0, :lo12:.LC2
        bl      puts
        mov     w0, 0
        ldp     x29, x30, [sp], 32
        ret