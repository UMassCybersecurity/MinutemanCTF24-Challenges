.LC0:
        .string "enter the activation code:"
.LC1:
        .string "%8s"
.LC2:
        .string ""
main:
        stp     x29, x30, [sp, -64]!
        adrp    x0, .LC0
        add     x0, x0, :lo12:.LC0
        mov     x29, sp
        stp     x19, x20, [sp, 16]
        add     x19, sp, 56
        mov     x20, 0
        str     x21, [sp, 32]
        adrp    x21, .LANCHOR0
        add     x21, x21, :lo12:.LANCHOR0
        str     xzr, [sp, 56]
        bl      puts
        add     x1, sp, 56
        adrp    x0, .LC1
        add     x0, x0, :lo12:.LC1
        bl      __isoc99_scanf
.L2:
        ldrb    w1, [x19, 7]
        sub     x19, x19, #1
        ldrb    w0, [x20, x21]
        add     x20, x20, 1
        eor     w0, w0, w1
        and     w0, w0, 255
        bl      putchar
        cmp     x20, 8
        bne     .L2
        adrp    x0, .LC2
        add     x0, x0, :lo12:.LC2
        bl      puts
        ldr     x21, [sp, 32]
        mov     w0, 0
        ldp     x19, x20, [sp, 16]
        ldp     x29, x30, [sp], 64
        ret
trinity:
        .ascii  "\020\002\022B\004\036_\r"