#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>

#include "sim_avr.h"
#include "uart_file.h"
#include "avr_uart.h"

/*
 * called when a byte is send via the uart on the AVR
 */
static void uart_file_in_hook(struct avr_irq_t * irq, uint32_t value, void * param)
{
	uart_file_t *uart = (uart_file_t *)param;
	putc(value, uart->output_file);
}


static const char * irq_names[1] = {
	[IRQ_UART_FILE_BYTE_IN] = "8<uart_file.in",
};

void uart_file_init(struct avr_t * avr, uart_file_t *p, char *output_path)
{
    p->output_file=fopen(output_path, "ab");
    if(! p->output_file){
        fprintf(stderr, "UART file ERROR: failed to open or create file. Init failed.\n");
        return;
    }
	setvbuf(p->output_file, NULL, _IONBF, 0); //disable buffering

	p->irq = avr_alloc_irq(&avr->irq_pool, 0, 1, irq_names);
	avr_irq_register_notify(p->irq + IRQ_UART_FILE_BYTE_IN, uart_file_in_hook, p);
}

void uart_file_attach(struct avr_t *avr, uart_file_t *p, char uart)
{
	// disable the stdio dump, as we are sending binary there
	uint32_t f = 0;
	avr_ioctl(avr, AVR_IOCTL_UART_GET_FLAGS(uart), &f);
	f &= ~AVR_UART_FLAG_STDIO;
	avr_ioctl(avr, AVR_IOCTL_UART_SET_FLAGS(uart), &f);

	avr_irq_t * src = avr_io_getirq(avr, AVR_IOCTL_UART_GETIRQ(uart), UART_IRQ_OUTPUT);

	if (!src) {
        fprintf(stderr, "UART file ERROR: failed to get uart IRQ. Attach failed.\n");
        return;
    }

	avr_connect_irq(src, p->irq + IRQ_UART_FILE_BYTE_IN); 
}

uint8_t uart_file_clear(uart_file_t *p){
	if(p->output_file){
		if(freopen(NULL, "wb", p->output_file) == NULL)
			return 1;
		setvbuf(p->output_file, NULL, _IONBF, 0); //disable buffering
	}
	return 0;
}

void uart_file_cleanup(uart_file_t *p){
    if(p->output_file)
        fclose(p->output_file);
}