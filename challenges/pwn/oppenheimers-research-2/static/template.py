from pwn import *

if args.REMOTE:
    host = "34.75.76.65"
    port = 9003
    p = remote(host, port)
else:
    p = process("./oppenheimers-research-2")
