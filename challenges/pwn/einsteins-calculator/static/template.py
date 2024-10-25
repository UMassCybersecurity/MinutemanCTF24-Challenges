from pwn import *

if args.REMOTE:
    host = "pwn-challenges.minuteman.umasscybersec.org"
    port = 9002
    p = remote(host, port)
else:
    p = gdb.debug('./einsteins-calculator')

p.interactive()
