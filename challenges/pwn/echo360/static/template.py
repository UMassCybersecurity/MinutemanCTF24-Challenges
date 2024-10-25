from pwn import *

if args.REMOTE:
    host = "pwn-challenges.minuteman.umasscybersec.org"
    port = 9001
    p = remote(host, port)
else:
    p = gdb.debug('./echo360')

p.interactive()
