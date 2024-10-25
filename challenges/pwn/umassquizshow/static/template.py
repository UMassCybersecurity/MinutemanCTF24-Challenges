from pwn import *

context.arch = 'amd64'
if args.REMOTE:
    host = "pwn-challenges.minuteman.umasscybersec.org"
    port = 9005
    p = remote(host, port)
else:
    p = process("./static/umass_quiz_show")