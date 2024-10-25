from Crypto.Util.number import getPrime, getRandomRange
from Crypto.Random import get_random_bytes

def crt_challenge(modulus_size, modulus_count):
    primes = set()
    # generate a bunch of primes
    while len(primes) < modulus_count:
        primes.add(getPrime(modulus_size))

    # take their product
    product = 1
    for p in primes:
        product *= p

    # generate a number less than their product
    key = getRandomRange(0, product)
    for p in primes:
        print(f"key % {p} = {key % p}")

    guess = int(input("What could the value of key be?"))

    # check if the guess matches the congruences
    for p in primes:
        if guess % p != key % p:
            print("That's not the key!")
            exit(0)


def cube_challenge():
    # generate the cube of a large number
    target = pow(getPrime(512), 3)
    print(f"key ** 3 = {target}")


    guess = int(input("What can the value of key be?"))

    # check if cubing the guess matches target
    if pow(guess, 3) != target:
        print("That's not the key!")
        exit(0)


def load_mailing_list():
    with open('public_keys.txt', 'r') as f:
        return [int(key) for key in f.readlines()]


def load_flag():
    with open('flag.txt', 'rb') as f:
        return f.readline()


if __name__ == '__main__':
    print("Chinese Remainder Theorem allows us to merge congruences!")
    print("Let's start off with small numbers, and with only 2 factors:")
    crt_challenge(10, 2)
    print("Nice! Now let's ramp up the challenge a little bit!")
    crt_challenge(50, 4)
    print("Awesome! But can you take the cube root of a large number?")
    cube_challenge()

    print("Great! Finally, let's break a poor implementation of RSA!")
    FLAG = load_flag() + get_random_bytes(20)
    assert len(FLAG) < 128
    mailing_list = load_mailing_list()
    e = 0x101
    for n in mailing_list:
        print(pow(int.from_bytes(FLAG, 'big'), e, n))


# solves crt for 2 modulus
def crt(m1, m2, r1, r2):
    return (pow(m2, -1, m1) * m2 * r1 + pow(m1, -1, m2) * m1 * r2) % (m1 * m2)

# solves crt for any number of modulus
def multi_crt(ms: list[int], rs: list[int]):
    # while there's still things to merge
    while len(ms) > 1:
        m1 = ms.pop(0)
        m2 = ms.pop(0)
        r1 = rs.pop(0)
        r2 = rs.pop(0)
        # merge the modulus via taking their LCM (assuming they're coprime, this is the same as their product)
        ms.append(m1 * m2)
        # merge the remainders using CRT on 2 modulus
        rs.append(crt(m1, m2, r1, r2))
    return rs[0]


# take the integer cube root of super large numbers
def binary_search_root(target):
    low = 0
    high = 1 << 512
    # cube-root-ing is hard, but cubing is easy.
    # since x < y if and only if x ** 3 < y ** 3, we can think of the cube function as a sorted array, and binary search!
    # so if we did have an array, arr[n] should store n ** 3.
    # we don't need to store the whole array though, since we can just calculate the needed values on demand.
    while high >= low:
        mid = (high + low) // 2
        val = pow(mid, 3)
        if val < target:
            low = mid + 1
        elif val > target:
            high = mid - 1
        else:
            return mid
    return low
