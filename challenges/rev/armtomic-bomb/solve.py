from pwn import *

e = ELF("./armtomic-bomb")

context.terminal = ['tmux', 'splitw', '-h']
p = gdb.debug("./armtomic-bomb", gdbscript = '''
          b phase1
          b phase2
          b phase3
          b phase4
          ''')
p.interactive()