from pwn import *

if args.REMOTE:
    host = "challs.umasscybersec.org"
    port = 1337
    p = remote(host, port)
else:
    e = ELF("./static/wormhole")
    context.terminal = ["tmux","splitw","-h"]
    p = process(e.path)