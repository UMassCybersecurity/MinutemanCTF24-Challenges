#include <math.h>

#include "utils.h"
#include <sim_avr.h>

double get_time(
		avr_t* avr)
{
    return (double)avr->cycle/avr->frequency;
}

/*
 * Returns the number of bytes required to address a specfic size
 * Ex: get_bytes(128) -> 1, get_bytes(1020) -> 2
 */
int get_bytes(
        int size)
{
    return ceil((log(size)/log(2))/8);
}

/*
 * Gets the file size (in bytes) by going to the end then back to the start
 * Note: this will reset the file to the beginning 
 */
size_t get_file_size(
        FILE *file)
{
    fseek(file, 0, SEEK_END); // seek to end of file
    size_t size = (size_t) ftell(file); // get current file pointer
    fseek(file, 0, SEEK_SET); // seek back to beginning of file
    
    return size;
}