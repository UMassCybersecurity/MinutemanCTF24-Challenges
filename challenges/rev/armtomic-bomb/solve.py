from pwn import *

e = ELF("./armtomic-bomb")

context.terminal = ['tmux', 'splitw', '-h']
p = gdb.debug("./armtomic-bomb", gdbscript = '''
        set emulate off
          b phase2
          b phase3
          b phase4
          ''')
p.sendline(b'112')
p.sendline(b'130')
p.interactive()