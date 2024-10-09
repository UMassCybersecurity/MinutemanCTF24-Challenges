#include <stdio.h>
#include <dirent.h> 
#include <string.h>
#include <stdlib.h>

#include "ctf_challenge.h"

#include "utils.h"

#define USER_DATA_PATH "./data/user"

#define LOG_BASE_PATH "./data/log"
#define LOG_UART_PATH LOG_BASE_PATH "/uart.txt"
#define LOG_ERROR_PATH LOG_BASE_PATH "/error.txt"

#define COMMANDS 13
/*
// Command structure
RX 1 byte: cmd(4 LSB) and flags(4 MSB)
... Transactions ...
End Transaction

// RX Transaction structure
TX 1 byte: Transaction type/flags (0x00)
RX 4 bytes: Transaction size
TX 1 byte: AKN or error(ends transaction)
RX n bytes: Transaction
TX 1 byte: AKN or error(ends transaction)

// TX Transaction structure
TX 1 byte: Transaction type/flags (0x01)
TX 4 bytes: Transaction size
RX 1 byte: AKN or error(ends transaction)
TX n bytes: Transaction
RX 1 byte: AKN or error(ends transaction)

// End Transaction structure
TX 1 byte: Transaction type (4 LSB)(0x2), return code (4 MSB)

cmd: (4 LSB)
0x00 upload firmware
0x01 list firmware
0x02 load firmware
0x03 sim start
0x04 sim stop
0x05 sim reset
0x06 sim reset perfs
0x07 get state
0x08 get uart log
0x09 clear uart log
0x0a get error log
0x0b clear error log
0x0c get flag
flag: (4 LSB) (unused rn)

Return
0x00 Ok
0x01 Transaction error
0x02 Operation error
*/

enum {
	RX_TRANSACTION,
	TX_TRANSACTION,
	END_TRANSACTION
};

enum {
	OK,
	TRANSACTION_ERROR,
	OPERATION_ERROR,
	LOCKED
};

ctf_challenge_environment_t env;

//////////////////////
// Command Handlers //
//////////////////////
/*
 * Completes a transaction to get data and puts it on the heap
 * The size of the data recived will be put into size if not null
 * If padding is added it will null terminate the data
 */
uint8_t get_data(void **buffer_ptr, uint8_t padding, size_t *recv_size){
	putc(RX_TRANSACTION, stdout);
	
	size_t size = 0;
	size_t recv = fread(&size, 4, 1, stdin);
	if(!recv){
		putc(TRANSACTION_ERROR, stdout);
		return TRANSACTION_ERROR;
	}
	
	*buffer_ptr = malloc(size + padding);
	if(*buffer_ptr == NULL){
		putc(OPERATION_ERROR, stdout);
		return OPERATION_ERROR;
	}

	putc(OK, stdout);

	recv = fread(*buffer_ptr, size, 1, stdin);
	if(!recv){
		putc(TRANSACTION_ERROR, stdout);
		return TRANSACTION_ERROR;
	}

	if(padding)
		*(char*)((long)*buffer_ptr + size) = 0;

	if(recv_size != NULL)
		*recv_size=size;

	putc(OK, stdout);
	return OK;
}

/*
 * Completes a transaction to send data
 * size is how much data you want to send
 */
uint8_t send_data(void *buffer, size_t size){
	putc(TX_TRANSACTION, stdout);
	fwrite(&size, 4, 1, stdout);

	uint8_t recv = getc(stdin);
	if(recv != OK)
		return TRANSACTION_ERROR;
	
	recv = fwrite(buffer, size, 1, stdout);
	
	char ret = getc(stdin);
	return ret;
}

uint8_t send_file(char *path){
	FILE *file = fopen(path, "rb");
	if(!file){
		return OPERATION_ERROR;
	}

	size_t size = get_file_size(file);

	if(size == 0) // if size is 0 then we don't need to read it
		return send_data(NULL, 0);

	uint8_t* buffer = malloc(size);
	if(buffer == NULL){
		fclose(file);
		return OPERATION_ERROR;
	}

	uint8_t ret = fread(buffer, size, 1, file);
	if(!ret){
		fclose(file);
		free(buffer);
		return OPERATION_ERROR;
	}
	
	uint8_t status = send_data(buffer, size);

	fclose(file);
	free(buffer);

	return status;
}

uint8_t handle_upload(uint8_t data){
	char *buffer = NULL;
	size_t file_name_size = 0;
	uint8_t status = get_data((void **)&buffer, 1, &file_name_size);
	if(status != OK){
		if(buffer != NULL)
			free(buffer);
		fprintf(stderr, "command ERROR: firmware upload: Unable to get file name.\n");	
		return status;
	}
	
	char path[sizeof(USER_DATA_PATH) + 1 + file_name_size];
	sprintf(path, "%s/%s", USER_DATA_PATH, buffer);

	free(buffer);
	buffer = NULL;

	FILE *firmware_file = fopen(path, "wb");
	if(!firmware_file){
		fprintf(stderr, "command ERROR: firmware upload: Unable to open file %s.\n", path);	
		return OPERATION_ERROR;
	}

	size_t file_size = 0;
	status = get_data((void**)&buffer, 0, &file_size);
	if(status != OK){
		if(buffer != NULL)
			free(buffer);
		fprintf(stderr, "command ERROR: firmware upload: Unable to get file data.\n");	
		return status;
	}

	fwrite(buffer, file_size, 1, firmware_file);
	fclose(firmware_file);
	free(buffer);

	return OK;
}

uint8_t handle_list(uint8_t data){
	DIR *d;
  	struct dirent *dir;
  	d = opendir(USER_DATA_PATH);
	if(!d){
		fprintf(stderr, "command ERROR: fimware list: Unable to open user directory.");	
		return OPERATION_ERROR;
	}

	while ((dir = readdir(d)) != NULL) {
		if(strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0)
			continue;
		
		uint8_t recv = send_data(dir->d_name, strlen(dir->d_name));
		if(recv != OK){
			closedir(d);
			return recv;
		}
	}
    closedir(d);

	return OK;
}

uint8_t handle_load(uint8_t data){
	char *file_name;
	size_t file_name_size = 0;
	uint8_t status = get_data((void**)&file_name, 1, &file_name_size);
	if(status != OK){
		if (file_name != NULL) 
			free(file_name);
		fprintf(stderr, "command ERROR: firmware load: Unable to get file name.");	
		return status;
	}
	
	char path[sizeof(USER_DATA_PATH) + 1 + file_name_size];
	sprintf(path, "%s/%s", USER_DATA_PATH, file_name);

	free(file_name);

	ctf_challenge_load_firmware(&env, path);

	return OK;
}

uint8_t handle_start(uint8_t data){
	if(ctf_challenge_start(&env)) //If start failed
		return OPERATION_ERROR;
	
	return OK;
}

uint8_t handle_stop(uint8_t data){
	ctf_challenge_stop(&env);
	return OK;
}

uint8_t handle_reset(uint8_t data){
	ctf_challenge_reset(&env);
	return OK;
}

uint8_t handle_reset_perfs(uint8_t data){
	if(ctf_challenge_reset_perfs(&env)) //If reset failed
		return OPERATION_ERROR;
	return OK;
}

uint8_t handle_get_state(uint8_t data){
	putc(env.avr->state, stdout);
	return OK;
}

uint8_t handle_get_uart_log(uint8_t data){
	uint8_t status = send_file(LOG_UART_PATH);
	if(status != OK)
		fprintf(stderr, "command ERROR: log uart: Unable to send uart file.\n");
	return status;
}

uint8_t handle_clear_uart_log(uint8_t data){
	if(uart_file_clear(&env.uart)) // clear error
		return OPERATION_ERROR;
	return OK;
}

uint8_t handle_get_error_log(uint8_t data){
	uint8_t status = send_file(LOG_ERROR_PATH);
	if(status != OK)
		fprintf(stderr, "command ERROR: log error: Unable to send error file.\n");
	return status;
}

uint8_t handle_clear_error_log(uint8_t data){
	if(freopen(NULL, "w", stderr) == NULL)
		return OPERATION_ERROR;
	
	setvbuf(stderr, NULL, _IONBF, 0); //disable buffering
	return OK;
}

uint8_t handle_get_flag(uint8_t){	
	return send_data("UMASS{tHe_5ecrEt_4mula}", 23);
}

///////////////
// Main code //
///////////////

uint8_t (*cmd_handlers[COMMANDS])(uint8_t) = {
	handle_upload,
	handle_list,
	handle_load,
	handle_start,
	handle_stop,
	handle_reset,
	handle_reset_perfs,
	handle_get_state,
	handle_get_uart_log,
	handle_clear_uart_log,
	handle_get_error_log,
	handle_clear_error_log,
	handle_get_flag
};

int main(int argc, char const* argv[])
{	
	freopen(LOG_ERROR_PATH, "a", stderr); //redirect stderr
	setvbuf(stderr, NULL, _IONBF, 0); //disable buffering

	freopen(NULL, "rb", stdin); //reopen stdin in byte mode
	freopen(NULL, "wb", stdout); //reopen stdout in byte mode
	setvbuf(stdout, NULL, _IONBF, 0); //disable buffering
	
	ctf_challenge_init(&env, LOG_UART_PATH);

	while(1){
		int data = getc(stdin);
		if(data == EOF)
			continue;
		uint8_t cmd = data & 0x0f;
		if(cmd >= COMMANDS){
			fprintf(stderr, "command ERROR: Unknown command %x.\n", cmd);
			putc(0x02 + OPERATION_ERROR << 4, stdout);
			continue;
		}
		if(data != cmd)
			fprintf(stderr, "command WARN: Flag bits are set but have no use.\n");
		
		putc(0x02 | (*cmd_handlers[cmd])(data) << 4, stdout);
	}

	ctf_challenge_cleanup(&env);

	fclose(stderr);
	fclose(stdin);
	fclose(stdout);
}