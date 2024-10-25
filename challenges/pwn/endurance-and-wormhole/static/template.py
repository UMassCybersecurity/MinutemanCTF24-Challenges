from pwn import *

if args.REMOTE:
    host = "pwn-challenges.minuteman.umasscybersec.org"
    port = 9004
    p = remote(host, port)
else:
    e = ELF("./wormhole")
    p = process(e.path)