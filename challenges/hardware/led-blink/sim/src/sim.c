#include <stdio.h>
#include <string.h>
#include <math.h>

#include "sim.h"
#include "sim_elf.h"
#include "avr_ioport.h"

static void led_in_hook( struct avr_irq_t *irq, uint32_t value, void *param)
{
    sim_instance_t *inst = param;
    float time = get_time(inst->avr);
    float delta = time - inst->last_pin_change;
    inst->last_pin_change = time;

    if(fabs(delta - SIM_TARGET_DELAY) > SIM_TOLERANCE){
        inst->time_valid = 0;
        return;
    }

    inst->time_valid += delta;
    if(inst->time_valid >= SIM_TIME_THRESHOLD)
        inst->flag_unlocked = 1;
}

float get_time(avr_t* avr) {
    return (float)avr->cycle / avr->frequency;
}

sim_return run_sim(char* firmware_path){
    // Load firmware 
    elf_firmware_t firmware = {{0}};
    
    int ret = elf_read_firmware(firmware_path, &firmware);
    if(ret != 0){
        fprintf(stderr, "Failed to open firmware at '%s'.\n", firmware_path);
        return LOAD_ERROR;
    }

    strcpy(firmware.mmcu, MCU);
    firmware.frequency = FREQ;

    // Create sim
    sim_instance_t inst;
    memset(&inst, 0, sizeof(inst));

    inst.avr = avr_make_mcu_by_name(MCU);
    if(inst.avr == NULL) {
        fputs("Failed to make MCU.", stderr);
        return LOAD_ERROR;
    }
    ret = avr_init(inst.avr);
    if(ret != 0){
        fputs("Failed to initialize MCU.", stderr);
        return LOAD_ERROR;
    }
    avr_load_firmware(inst.avr, &firmware);

    static const char * _led_irq_names[1] = {
	    "<led-1.in"
    };
    avr_irq_t *led_irq = avr_alloc_irq(&inst.avr->irq_pool, 0, 1, _led_irq_names);
    if(led_irq == NULL) {
        fputs("Failed to allocate IRQ.", stderr);
        return LOAD_ERROR;
    }
    avr_irq_register_notify(led_irq, led_in_hook, &inst);
    avr_connect_irq(avr_io_getirq(inst.avr, AVR_IOCTL_IOPORT_GETIRQ('B'), 0), led_irq);

    inst.avr->state = cpu_Running;
    int state = cpu_Running;
    while ((state != cpu_Done) && (state != cpu_Crashed) && (get_time(inst.avr) < SIM_TIMEOUT) && !inst.flag_unlocked){
        state = avr_run(inst.avr);
    }

    if(inst.flag_unlocked)
        return FLAG_UNLOCKED;
    else if(state == cpu_Crashed)
        return SIM_ERROR;
    else
        return FLAG_LOCKED;
}