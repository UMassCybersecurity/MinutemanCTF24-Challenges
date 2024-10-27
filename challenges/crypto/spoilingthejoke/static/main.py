import string

def load_flag():
    with open('flag.txt', 'r') as f:
        return f.read()


def load_key():
    with open('key.txt', 'r') as f:
        return f.read()

# this is a classic Vigenère cipher (all non-letters are simply skipped).
def encrypt(msg, key):
    cip = ''
    for c in msg:
        if c in string.ascii_lowercase:
            cip += chr(((ord(c) - ord('a')) + (ord(key[0]) - ord('a'))) % 26 + ord('a'))
            key = key[1:] + key[:1]
        elif c in string.ascii_uppercase:
            cip += chr(((ord(c) - ord('A')) + (ord(key[0]) - ord('a'))) % 26 + ord('A'))
            key = key[1:] + key[:1]
        else:
            cip += c
    return cip


# for your convenience?
def decrypt(msg, key):
    cip = ''
    for c in msg:
        if c in string.ascii_lowercase:
            cip += chr(((ord(c) - ord('a')) - (ord(key[0]) - ord('a'))) % 26 + ord('a'))
            key = key[1:] + key[:1]
        elif c in string.ascii_uppercase:
            cip += chr(((ord(c) - ord('A')) - (ord(key[0]) - ord('a'))) % 26 + ord('A'))
            key = key[1:] + key[:1]
        else:
            cip += c
    return cip

if __name__ == '__main__':

    # The file given was originally in English. There are quite a few 1-letter word in there. English doesn't have a lot of those.
    # English also doesn't have many letters that often go after apostrophes, among many other linguistic features you
    # can use to your advantage.

    FLAG = load_flag()
    k = load_key()
    with open('output.txt', 'w') as f:
        # The key has length 10
        f.write(str(len(k)))
        f.write('\n')
        f.write(encrypt(FLAG, k))
