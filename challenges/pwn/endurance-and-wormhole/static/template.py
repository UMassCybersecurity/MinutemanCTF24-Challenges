from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9004
    p = remote(host, port)
else:
    e = ELF("./wormhole")
    p = process(e.path)