#include <pthread.h>

#include <sim_avr.h>

#include "uart_file.h"

typedef struct ctf_challenge_environment_t
{
        avr_t * avr;
	pthread_t avr_thread;
        volatile uint8_t running;

        uart_file_t uart;
} ctf_challenge_environment_t;

void ctf_challenge_init(
        ctf_challenge_environment_t* env, 
	char* uart_path );

void ctf_challenge_load_firmware(
        ctf_challenge_environment_t* env,
        char* firmware_path );

uint8_t ctf_challenge_start(
        ctf_challenge_environment_t* env );

void ctf_challenge_stop(
        ctf_challenge_environment_t* env );

void ctf_challenge_reset(
        ctf_challenge_environment_t* env );

void ctf_challenge_cleanup(
	ctf_challenge_environment_t* env);