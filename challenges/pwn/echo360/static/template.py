from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9001
    p = remote(host, port)
else:
    p = gdb.debug('./echo360')

p.interactive()
