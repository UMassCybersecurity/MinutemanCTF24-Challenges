import random
from datetime import datetime


def get_time():
    return datetime.utcnow().isoformat(timespec='microseconds')


def xor(msg, key):
    return bytes([m ^ k for m, k in zip(msg, key)])


def encrypt(msg):
    random.seed(get_time())
    return xor(msg, random.randbytes(len(msg)))


def send_message(msg):
    print(f'The server sent the message "{msg}" at time {get_time()}')


def receive_message():
    choice = input()
    print(f'The server received the message "{choice}" at time {get_time()}')
    return choice


def load_flag():
    with open('flag.txt', 'rb') as f:
        return f.readline()


if __name__ == '__main__':
    send_message("commence temporal pincer maneuver?")
    name = receive_message()
    send_message(f"ok, {name}, here's the flag (encrypted for safety purposes of course): {encrypt(load_flag()).hex()}")
