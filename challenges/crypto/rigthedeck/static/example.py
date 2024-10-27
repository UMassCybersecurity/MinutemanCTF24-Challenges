# This file outlines basically all the steps needed to execute the protocol with the server, as an honest player.
# Of course, you're not exactly supposed to be honest with the server, but you also can't outright violate the agreed
# upon protocol. The server will refuse to play the game if they don't have aces in their hand.

# You'll only win if the server have quads AND you have a royal flush by the end of the round.


# this might come in handy for figuring out which rank is which...
def analyze(ranks):
    analysis = {}
    for x, y in itertools.combinations(ranks, 2):
        if x not in analysis:
            analysis[x] = set()
        analysis[x].add(x ^ y)
        if y not in analysis:
            analysis[y] = set()
        analysis[y].add(x ^ y)
    return analysis

# actual code to talk to the server

from pwn import *
from main import *

p = process(['python3', 'main.py'])

# skip the intro
p.recvuntil(b'which:\n')

# receive the deck
deck = json.loads(p.recvline())

# TODO: rig the game by manipulating the cards here.
# TODO: you need the server to have aces, and also give them have quad aces by the end, while giving yourself a royal flush.

# make our own random key
key = urandom(4)

# turn the hex encoded cards back into bytes
deck = [bytes.fromhex(card) for card in deck]

# encrypt the deck ourselves
deck = [xor(card, key).hex() for card in deck]

# shuffle the deck ourselves
random.seed(urandom(16))
random.shuffle(deck)

# TODO: you could read the rest of the code, but all you can really do to win is change the few lines above

# send the result back to the server
p.sendline(json.dumps(deck).encode())

# skip until the server gives the deck
p.recvuntil(b'away!\n')

# receive the deck
deck = json.loads(p.recvline())

# remove our global key and encrypt each card individually
individual_keys = [urandom(4) for _ in range(52)]
deck = [bytes.fromhex(card) for card in deck]
deck = [xor(card, key) for card in deck]
deck = [xor(card, ind_key).hex() for card, ind_key in zip(deck, individual_keys)]
p.sendline(json.dumps(deck).encode())

# skip until we get the hashes
p.recvuntil(b'secrecy:\n')

# receive the hashes
hashes = json.loads(p.recvline())

# send our own hashes over
p.sendline(json.dumps([sha256(key).hexdigest() for key in individual_keys]).encode())

# skip until we get the keys
p.recvuntil(b'them!\n')

# put the keys into the right position (so i can reuse my code lmao)
keys = json.loads(p.recvline())
keys = [b''] * 2 + [bytes.fromhex(key) for key in keys]

# check if the keys actually makes sense
if any(sha256(keys[i]).hexdigest() != hashes[i] for i in range(2, 4)):
    print("the server gave you the wrong keys!")

# use the key to see what your own cards are
deck = [bytes.fromhex(card) for card in deck]

your_cards = [xor(xor(deck[i], keys[i]), individual_keys[i])[1:3].decode() for i in range(2, 4)]
print(f'your cards are: {your_cards}')

# skip until we're prompted to give our keys
p.recvuntil(b'them!')

# send the server the correct keys
p.sendline(json.dumps([individual_keys[0].hex(), individual_keys[1].hex()]).encode())

line = p.recvline()
if line == b'welp, my cards are terrible, so imma fold, but you get how the system works now, right?\n':
    print("unfortunately, the server folded early =((")
    exit(0)

keys = json.loads(p.recvline())
keys = [b''] * 4 + [bytes.fromhex(key) for key in keys]

# check if the keys actually makes sense
if any(sha256(keys[i]).hexdigest() != hashes[i] for i in range(4, 9)):
    print("the server gave you the wrong keys!")

# use the key to see what the streets are
streets = [xor(xor(deck[i], keys[i]), individual_keys[i])[1:3] for i in range(4, 9)]
print(streets)

# skip until we're prompted to give our keys
p.recvuntil(b'them!')

# send the server the correct keys
p.sendline(json.dumps([individual_keys[4].hex(), individual_keys[5].hex(), individual_keys[6].hex(), individual_keys[7].hex(),individual_keys[8].hex()]).encode())

line = p.recvline()
if line == b'aw man, the rollout sucks. imma stop here.\n':
    print("unfortunately, the server folded early =((")
    exit(0)

p.recvuntil(b'baby!\n')

keys = json.loads(p.recvline())
keys = [bytes.fromhex(key) for key in keys]

# check if the keys actually makes sense
if any(sha256(keys[i]).hexdigest() != hashes[i] for i in range(2)):
    print("the server gave you the wrong keys!")

# use the key to see what the streets are
server_hand = [xor(xor(deck[i], keys[i]), individual_keys[i])[1:3] for i in range(2)]
print(server_hand)

# skip until we're prompted to give our keys
p.recvuntil(b'wins!')

# send the server the correct keys
p.sendline(json.dumps([individual_keys[2].hex(), individual_keys[3].hex()]).encode())

p.interactive()