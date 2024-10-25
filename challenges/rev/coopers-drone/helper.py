# RNG params
A = 0x19660d
B = 0x3c6ef35f
CUR = 0

FLAG = b"MINUTEMAN{what's_a_calling_convention?}"

def srand(seed):
    global CUR
    CUR = seed

def rand():
    global CUR
    n = (A*CUR + B) % 2**32
    CUR = n
    return n

def crypt(ct):
    chars = [ct[i] ^ (rand() & 0xFF) for i in range(len(ct))]
    return chars


# ans: 1850484176
if __name__ == "__main__":
    seed = 0x6e4c25d0
    srand(seed)

    print(f"First rand number: {hex(rand())}  (should be 0xdeadbeef)")

    encrypted = ""
    for x in crypt(FLAG):
        encrypted += hex(x) + ", "

    print(f"Flag          : {FLAG}")
    print(f"Encrypted flag: {encrypted}")
