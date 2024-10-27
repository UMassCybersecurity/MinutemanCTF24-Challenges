
section .data
    prompt db 'Enter the secret key: ', 0 
    err_msg db 'Invalid input character encountered', 10, 0 ; newline + null
    fail_msg db 'Wrong key, try again!', 10, 0 ; newline + null
    ciphertext db 0xcf, 0xb0, 0x4a, 0xc6, 0x82, 0x78, 0x35, 0x36, 0x24, 0xba, 0x5b, 0xf3, 0x5f, 0xf1, 0x7, 0x8c, 0xd, 0xe8, 0xb, 0xc0, 0xc7, 0xa1, 0xa4, 0xee, 0x54, 0x36, 0x23, 0xc8, 0x61, 0x7b, 0x6, 0x6a, 0x4c, 0x6d, 0xcd, 0xdc, 0x18, 0x62, 0x65


section .bss
    buffer resb 33  ; buffer for user input
    seed   resq 1   ; global RNG seed
    rmult  resq 1   ; global RNG multiplier
    roffs  resq 1   ; global RNG offset


section .text
    global _start


; Custom calling convention:
; First arg goes in rbp
; second arg pushed on the stack
; third arg goes in xmm0
; ret value in rcx

; void srand(int seed, int mult, int offset)
srand:
    xor rax, rax
    mov [seed], rbp
    mov r13, [rsp + 0x8]
    mov [rmult], r13
    movups [roffs], xmm0
    ret


; int rand()
; returns rmult*cur_seed + roffs (mod 2^32)
rand:
    xor rax, rax
    mov rcx, [seed]
    mov r13, [rmult]
    imul rcx, r13
    add rcx, [roffs]
    and dword ecx, 0xffffffff
    mov [seed], rcx
    ret 


; int decrypt(char* ciphertext, int len)
decrypt:
    xor r12, r12
    .dec_loop:
        cmp r12, [rsp + 0x8]
        jz .done

        ; Decrypt one byte of string
        call rand
        xor byte [rbp + r12], cl
   
        inc r12
        jmp .dec_loop
    .done:
        ret


; int str_to_int(char* str)
str_to_int:
    xor rcx, rcx
    .convert_loop:
        movzx r13, byte [rbp]
        cmp r13, 10              ; Check for newline
        jz    .done

        sub   r13, '0'          ; Convert ASCII character to integer (e.g., '0' -> 0, '1' -> 1, ...)
        cmp   r13, 9            ; Check if the character is valid (0-9)
        ja    .invalid_input

        ; Update result
        imul rcx, 10
        add rcx, r13

        inc   rbp
        jmp   .convert_loop
    .invalid_input:
        mov rbp, err_msg
        call print
        mov rcx, -1
    .done:
        ret   


; void get_input(char* buf)
get_input:
    xor rax, rax ; syscall 0 = read
    xor rdi, rdi ; fd = 0 = stdin
    mov rsi, rbp ; buffer
    mov rdx, 32  ; num bytes to read
    syscall
    mov byte [rbp + 32], 0 ; null terminate
    ret


; void print(char* buf)
print:
    ; Setup syscall stuff
    xor rax, rax
    xor rdi, rdi
    xor rdx, rdx
    inc rax         ; syscall number = 1
    inc rdi         ; fd = 1 = stdout

    ; Calculate length of string and then call write()
    xor r12, r12
    .len:
        cmp byte [rbp + r12],  0x0
        jz .end
        inc r12
        jmp .len
    .end:
        lea rsi, [rbp]  ; buffer
        mov rdx, r12    ; computed length
        syscall         ; write(stdout, buf, len)
        ret
    


_start:
    ; print prompt
    mov rbp, prompt
    call print
 
    ; Get user input
    mov rbp, buffer
    call get_input

    ; Convert input from string to integer
    mov rbp, buffer
    call str_to_int
    cmp rcx, -1
    je .done

    ; Seed RNG based on input
    mov rbp, rcx
    push 0x19660d
    mov r13, 0x3c6ef35f
    movq xmm0, r13
    call srand
    pop r13

    ; See if key is correct
    call rand
    cmp dword ecx, 0xdeadbeef
    jnz .fail
    ; Decrypt
    mov rbp, ciphertext
    push 39     ; ciphertext length
    call decrypt
    pop r13
    ; Print flag
    mov rbp, ciphertext
    call print
    jmp .done

    .fail:
        mov rbp, fail_msg
        call print
    .done:
        ; Call exit
        pop r13      ; cancels out random constant 1 on the stack
        mov rax, 60  ; syscall: exit
        mov rdi, 0   ; status
        syscall
