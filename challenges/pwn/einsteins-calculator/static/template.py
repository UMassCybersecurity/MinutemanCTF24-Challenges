from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9002
    p = remote(host, port)
else:
    p = gdb.debug('./einsteins-calculator')

p.interactive()
