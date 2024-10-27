import itertools
import json
import random
from os import urandom

from hashlib import sha256
def xor(card, key):
    return bytes([c ^ k for c, k in zip(card, key)])

def load_flag():
    with open('flag.txt', 'rb') as f:
        return f.readline()


if __name__ == '__main__':
    print("mental poker is played between 2 players, but no house is involved. neither trust the other, yet somehow the game must go on.")
    print("through multiple rounds of encryption, we can have both players shuffle the deck with neither knowing any of the cards")
    print("without the permission of the other player.")
    print()

    print("here is an example implementation. first, let's create a deck of cards:")
    cards = [''.join(card).encode() for card in itertools.product("23456789tjqka", "chds")]
    print(cards)
    print("for the most part, i'll give you the deck hex-encoded:")
    cards = [card.hex() for card in cards]
    print(cards)
    print("i'll add some noise to the cards so it's not too deterministic...")
    cards = [(urandom(1) + bytes.fromhex(card) + urandom(1)).hex() for card in cards]
    print(cards)

    print()
    print("i'll generate my own secret key, and encrypt all of the cards with it. then, i'll shuffle the deck so you can't tell which is which:")
    key = urandom(4)
    deck = [bytes.fromhex(card) for card in cards]
    deck = [xor(card, key).hex() for card in deck]
    random.seed(urandom(16))
    random.shuffle(deck)
    print(json.dumps(deck))

    deck = json.loads(input("now you should encrypt via XOR-ing with your own key, then shuffle, so that i can't tell what's going on either:"))
    deck = [bytes.fromhex(card) for card in deck]
    if not (isinstance(deck, list) and len(deck) == 52 and all(len(card) == 4 for card in deck)):
        print("you did some weird stuff that you weren't supposed to do there...")
        exit(0)

    print("great! now i'll remove my global encryption, and encrypt the individual cards instead. this way, i can reveal the key to each one without giving everything away!")
    individual_keys = [urandom(4) for _ in range(52)]
    deck = [xor(card, key) for card in deck]
    deck = [xor(card, ind_key).hex() for card, ind_key in zip(deck, individual_keys)]
    print(json.dumps(deck))

    deck = json.loads(input("now you should remove your global encryption, and encrypt the cards individually as well:"))
    deck = [bytes.fromhex(card) for card in deck]
    if not (isinstance(deck, list) and len(deck) == 52 and all(len(card) == 4 for card in deck)):
        print("you did some weird stuff that you weren't supposed to do there...")
        exit(0)

    print("finally, just to make sure you're not gonna pull a switcharoo on me later on, send me the hash of all of your keys in order!")
    print("of course, i'll do the same first. here are all of my keys, hashed for secrecy:")
    print(json.dumps([sha256(key).hexdigest() for key in individual_keys]))
    hashes = json.loads(input("give me the hashes for your keys:"))

    print("great! now we can play poker!")
    print("i'll give you the decryption key for your first 2 cards (the 3rd and 4th cards) so you can look at them!")
    print(json.dumps([individual_keys[2].hex(), individual_keys[3].hex()]))

    keys = json.loads(input("please give me the decryption keys for my first 2 cards (the 1st and 2nd cards) so i can look at them!"))
    keys = [bytes.fromhex(key) for key in keys]
    if any(sha256(keys[i]).hexdigest() != hashes[i] for i in range(2)):
        print("you gave me the wrong keys!")
        exit(0)

    hole_cards = [xor(xor(deck[i], keys[i]), individual_keys[i]) for i in range(2)]

    if any(card[1] != ord('a') for card in hole_cards):
        print("welp, my cards are terrible, so imma fold, but you get how the system works now, right?")
        exit(0)

    print("oooooh, let's play let's play! here are all of the keys for the next 5 cards:")
    print(json.dumps([individual_keys[4].hex(), individual_keys[5].hex(), individual_keys[6].hex(), individual_keys[7].hex(), individual_keys[8].hex()]))
    keys = json.loads(input("please give me the decryption keys for my those 5 cards so we can both look at them!"))
    keys = [b''] * 4 +[bytes.fromhex(key) for key in keys]
    if any(sha256(keys[i]).hexdigest() != hashes[i] for i in range(4, 9)):
        print("you gave me the wrong keys!")
        exit(0)
    streets = [xor(xor(deck[i], keys[i]), individual_keys[i]) for i in range(4, 9)]
    if sum(1 if card[1] == ord('a') else 0 for card in streets + hole_cards) != 4:
        print("aw man, the rollout sucks. imma stop here.")
        exit(0)
    print("oooooh im so confident that imma bet the flag itself!")
    print("you can have the keys for my cards now! quad aces baby!")
    print(json.dumps([individual_keys[0].hex(), individual_keys[1].hex()]))
    keys = json.loads(input("please give me the decryption keys for your 2 cards so we can both see who wins!"))
    keys = [b''] * 2 + [bytes.fromhex(key) for key in keys]
    if any(sha256(keys[i]).hexdigest() != hashes[i] for i in range(2, 4)):
        print("you gave me the wrong keys!")
        exit(0)
    players_card = [xor(xor(deck[i], keys[i]), individual_keys[i]) for i in range(2, 4)] + streets
    players_card = [card[1:3] for card in players_card]
    for suit in b'chds':
        royal_flush_hand = [bytes([rank, suit]) for rank in b'tjkqa']
        if all(card in players_card for card in royal_flush_hand):
            print("no shot you just did that! here's the flag:")
            print(load_flag())
            break
    else:
        print("hmph, i'm not giving up the flag unless you have a royal flush!")