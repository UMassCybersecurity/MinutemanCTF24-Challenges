from pwn import *

if args.REMOTE:
    host = "challs.umasscybersec.org"
    port = 2337
    p = remote(host, port)
else:
    p = gdb.debug('./einsteins-calculator')

p.interactive()
