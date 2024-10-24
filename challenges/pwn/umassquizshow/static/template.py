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