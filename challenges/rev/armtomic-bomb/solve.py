from pwn import *

e = ELF("./armtomic-bomb")

context.terminal = ['tmux', 'splitw', '-h']
p = gdb.debug("./armtomic-bomb", gdbscript = '''
        set emulate off
          ''')
#phase 1
p.sendline(b'112')
p.sendline(b'160')
#phase 2
p.sendline(b'0xFF00000000000000')
p.sendline(b'8')
#phase 3
p.sendline(b'0x9DCF929D')
#phase 4
p.sendline(b'defuz')
p.interactive()