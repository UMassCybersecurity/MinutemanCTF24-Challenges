from pwn import *

p = process('./echo360');

p.sendline(b"AAAABBBBCCCCDDDDEEEEFFFF");
print(p.recvline())
print(p.recvline())