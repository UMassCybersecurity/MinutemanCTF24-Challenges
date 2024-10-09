#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "avr_twi.h"
#include "avr_ioport.h"
#include "sim_elf.h"

#include "ctf_challenge.h"

#define MCU "atmega1280"
#define FREQ 16000000

void ctf_challenge_init(
        ctf_challenge_environment_t* env,
        char* uart_path )
{ 
    memset(env, 0, sizeof(*env));
	
    // AVR
    env->avr = avr_make_mcu_by_name(MCU);
    if (!env->avr) {
		fprintf(stderr, "CTF challenge ERROR: AVR Init failed!\n");
		return;
	}

    avr_init(env->avr);
    env->avr->state=cpu_Stopped;

    // uart
    uart_file_init(env->avr, &env->uart, uart_path);
    uart_file_attach(env->avr, &env->uart, '0');
}

void ctf_challenge_load_firmware(
        ctf_challenge_environment_t* env,
        char* firmware_path )
{
    //must reset environment for new firmware to run properly
    ctf_challenge_reset(env);
    
    elf_firmware_t f = {{0}};
    elf_read_firmware(firmware_path, &f);
    
    strcpy(f.mmcu, MCU);
    f.frequency=FREQ;
    
    avr_load_firmware(env->avr, &f);
}

void * ctf_challenge_run(void *param){
    avr_t *avr = (avr_t *)param;

    int state = avr->state;
    while(!(state==cpu_Crashed || state==cpu_Stopped || state==cpu_Done)){
        state = avr_run(avr);
    }
}

uint8_t ctf_challenge_start(
		ctf_challenge_environment_t* env )
{
    if(env->avr_thread) //If the thread is already running
        return 0;

    if(env->avr->state == cpu_Crashed || env->avr->state == cpu_Done){ //If crashed or done don't start
        fprintf(stderr, "CTF challenge WARN: Attempted to start a crashed or done microcontroller.");
        return 1;
    }

    env->avr->state=cpu_Running;
    return pthread_create(&env->avr_thread, NULL, ctf_challenge_run, env->avr);
}

/*
 * Sends a stop signal to the microcontroller and waits for thread to finish
 */
void ctf_challenge_stop(
		ctf_challenge_environment_t* env )
{
    if(!env->avr_thread)
        return;

    env->avr->state=cpu_Stopped;
    pthread_join(env->avr_thread, NULL);
    env->avr_thread=0;
}

void ctf_challenge_reset(
        ctf_challenge_environment_t* env)
{
    ctf_challenge_stop(env);
    avr_reset(env->avr);
    env->avr->state=cpu_Stopped;
}

void ctf_challenge_cleanup(
        ctf_challenge_environment_t *env)
{
    ctf_challenge_stop(env);

    uart_file_cleanup(&env->uart);

    avr_deallocate_ios(env->avr);
}