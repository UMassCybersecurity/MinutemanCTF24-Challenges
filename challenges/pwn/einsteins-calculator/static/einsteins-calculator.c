/*
author: leon
gcc -o einsteins-calculator -no-pie -Og src.c
*/

#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

typedef struct Calculator {
    int m;
    int c;
    int e;
    char overflow_flag;
    char underflow_flag;
    char division_by_zero_flag;
} Calculator;

void emc2(Calculator* calc) {
    calc->e = calc->m * calc->c * calc->c;
}

void add(Calculator* calc) {
    if (calc->m < 0 || calc->c < 0) {
        puts("You can't add negative numbers");
        return;
    }
    calc->e = calc->m + calc->c;
    if (calc->e < 0) {
        calc->overflow_flag = 1;
        puts("Oops, looks like we have an overflow here!");
    }
}

void sub(Calculator* calc) {
    if (calc->m > 0) {
        puts("you can't subtract from positive numbers");
        return;
    }
    if (calc->c < 0) {
        puts("you can't subtract with negative numbers");
        return;
    }
    calc->e = calc->m - calc->c;

    if (calc->e > 0) {
        calc->underflow_flag = 1;
        puts("Oops, looks like we have an underflow here!");
    }
}

void mul(Calculator* calc) {
    calc->e = calc->m * calc->c;
}

void divd(Calculator* calc) {
    if (calc->c == 0) {
        calc->division_by_zero_flag = 1;
        puts("Oops, looks like we have a division by zero here!");
    } else {
        calc->e = calc->m / calc->c;
    }
}

void print_calc(Calculator* calc) {
    printf("m = %d\n", calc->m);
    printf("c = %d\n", calc->c);
    printf("e = %d\n", calc->e);
}

void check_flags(Calculator* calc) {
    if (calc->overflow_flag) {
        puts("Overflow detected!");
    }
    if (calc->underflow_flag) {
        puts("Underflow detected!");
    }
    if (calc->division_by_zero_flag) {
        puts("Division by zero detected!");
    }
    emc2(calc);
    if (calc->overflow_flag && calc->underflow_flag && calc->division_by_zero_flag && calc->e == -1) {
        puts("Hmm, you broke einstein's calculator\n");
        if (system("cat flag.txt")) {
            puts("Something went wrong, contact admin!");
        }
    }
}

void print_menu() {
    puts("0.input value 1.add 2.subtract 3.multiply 4.divide 5.print values 6.print flags");
}

void input_val(Calculator* calc) {
    puts("input term 1:");
    scanf("%d", &calc->m);
    puts("input term 2:");
    scanf("%d", &calc->c);
}

int main() {
    Calculator einsteins_calculator = { 0, 0, 0, 0, 0, 0 };
    while (1) {
        print_menu();
        int sel = -1;
        scanf("%1d", &sel);
        switch (sel) {
        case 0:
            input_val(&einsteins_calculator);
            break;
        case 1:
            add(&einsteins_calculator);
            break;
        case 2:
            sub(&einsteins_calculator);
            break;
        case 3:
            mul(&einsteins_calculator);
            break;
        case 4:
            divd(&einsteins_calculator);
            break;
        case 5:
            print_calc(&einsteins_calculator);
            break;
        case 6:
            check_flags(&einsteins_calculator);
            break;
        default:
            return 0;
        }
    }
}
