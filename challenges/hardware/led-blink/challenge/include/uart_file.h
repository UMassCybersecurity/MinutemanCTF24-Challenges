#ifndef __UART_FILE_H___
#define __UART_FILE_H___

#include <stdio.h>

#include <sim_irq.h>

enum {
	IRQ_UART_FILE_BYTE_IN = 0,
};

typedef struct uart_file_t {
	FILE *output_file;
    avr_irq_t *	irq;		// irq list
} uart_file_t;

void uart_file_init(struct avr_t *avr, uart_file_t *p, char *output_path);

void uart_file_attach(struct avr_t *avr, uart_file_t *p, char uart);

uint8_t uart_file_clear(uart_file_t *p);

void uart_file_cleanup(uart_file_t *p);

#endif