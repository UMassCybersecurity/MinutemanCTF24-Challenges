#ifndef __UTILS_H___
#define __UTILS_H___

#include <stdio.h>

#include "sim_avr.h"

/*
 * Returns the time the avr simulation has been running.
 * This is calculated using clock cycles and frequency
 */
double get_time(
        struct avr_t *avr);

/*
 * Returns the number of bytes required to address a specfic size
 * Ex: get_bytes(128) -> 1, get_bytes(1020) -> 2
 */
int get_bytes(
    int size);

size_t get_file_size(
    FILE *size);

#endif