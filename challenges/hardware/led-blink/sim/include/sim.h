#ifndef __SIM_H__
#define __SIM_H__

#include "sim_avr.h"

#define MCU "atmega328p"
#define FREQ 16000000

#define SIM_TARGET_DELAY 0.1
#define SIM_TOLERANCE 0.005
#define SIM_TIME_THRESHOLD 3
#define SIM_TIMEOUT 5

typedef struct sim_instance_t {
    avr_t *avr;
    float last_pin_change;
    float time_valid;
    uint8_t flag_unlocked;

} sim_instance_t;

typedef enum sim_return{
    FLAG_UNLOCKED,
    FLAG_LOCKED,
    LOAD_ERROR,
    SIM_ERROR
} sim_return;

/*
 * Returns the time in seconds the avr simulation has been running.
 * This is calculated using clock cycles and frequency
 */
float get_time(avr_t *avr);

/*
 * Runs an AVR simulation using the firmware specified.
 * NOTE: mem leak rn!!
 */
sim_return run_sim(char *firmware_path);

#endif