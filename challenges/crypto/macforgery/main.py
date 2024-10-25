from hashlib import sha256
from Crypto.Util.number import getPrime


def verify_commands(msg, p, q):
    check, signature, commands = msg[:32], msg[32: 128 + 32], msg[128 + 32:]
    assert check == sha256(signature + commands).digest()
    assert pow(int.from_bytes(commands, 'big'), pow(0x10001, -1, (p-1) * (q-1)), p * q) == int.from_bytes(signature, 'big')
    return commands

def sign_commands(msg, p, q):
    signature = pow(int.from_bytes(msg, 'big'), pow(0x10001, -1, (p-1) * (q-1)), p * q).to_bytes(128, 'big')
    check = sha256(signature + msg).digest()
    return check + signature + msg

def load_flag():
    with open('flag.txt', 'rb') as f:
        return f.readline()

if __name__ == '__main__':
    p, q = getPrime(512), getPrime(512)
    print(f"The public key is {p * q}")
    commands = verify_commands(bytes.fromhex(input("Give me signed commands! (in hex):")), p, q)
    for command in commands.split(b','):
        if command == b'give_flag':
            print(load_flag())
        else:
            print("bad command, exiting...")
            exit(0)