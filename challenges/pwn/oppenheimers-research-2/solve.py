from sys import stdout

stdout.buffer.write(b'fffff\x00' + b'\x5f' * 250)