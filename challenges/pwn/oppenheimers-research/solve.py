import pwn

p = pwn.process("./static/oppenheimers-research")
# host = "localhost"
# port = 4444
# p = remote(host, port)

p.sendline(b'A' * 250)
p.interactive()