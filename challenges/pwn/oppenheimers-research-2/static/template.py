from pwn import *

if args.REMOTE:
    host = "pwn-challenges.minuteman.umasscybersec.org"
    port = 9003
    p = remote(host, port)
else:
    p = process("./oppenheimers-research-2")
