def encrypt(key, message):
    repeat_time = len(message) // len(key) + 1
    padded_key = key * repeat_time
    return bytes(x ^ y for x, y in zip(padded_key, message))


message = """<PUT PLAINTEXT HERE>""".encode()
key = """<PUT KEY HERE>""".encode()
print(encrypt(key, message).hex())
# With the values above, the output should be 00000000001b0918690611171d6a1c1810066575
