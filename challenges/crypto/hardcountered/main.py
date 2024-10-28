import json
from Crypto.Cipher import AES
from os import urandom


aes_key = urandom(16)


def encrypt(msg):
    cipher = AES.new(aes_key, AES.MODE_CTR)
    return cipher.encrypt(msg) + cipher.nonce


def decrypt(msg):
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=msg[-8:])
    msg = cipher.decrypt(msg[:-8])
    return msg


def load_flag():
    with open('flag.txt', 'rb') as f:
        return f.readline()


if __name__ == '__main__':
    print("we don't always need to fully decrypt a message to cause chaos. why know when you can tamper?")
    print("AES counter mode can properly keep secrets, but is not tamper-proof by itself.")
    print("the server wil give you a token that only it could have generated (since only it has the key).")
    print("give yourself admin privileges (change your 'type' to 'admin') to get the flag!")
    print("hint: try XOR-ing the ciphertext with stuff and see how the decrypted token changes!")
    # only the server will ever know this secret
    secret_database = {"Eve": urandom(16)}

    token = {"username": "Eve", "type": "user", "secret": secret_database["Eve"].hex()}
    text = json.dumps(token).encode()
    print(f"Session token: {encrypt(text).hex()}")
    inp = input("give me your token:")
    dec = decrypt(bytes.fromhex(inp))

    # in practice, no server will reveal this. it doesn't make this challenge easier, but it will make your life a bit easier hopefully
    print("the decrypted token is: ")
    token = json.loads(dec)
    print(token)
    if token["secret"] != secret_database[token["username"]].hex():
        print("incorrect secret!")
        exit(0)
    elif token["type"] != "admin":
        print("not the admin!")
        exit(0)
    else:
        print("welcome, admin! here's the flag:")
        print(load_flag())
