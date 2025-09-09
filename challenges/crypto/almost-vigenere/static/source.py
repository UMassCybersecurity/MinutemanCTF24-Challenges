# aA is 0, zZ is 25
letter_to_number = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
                    'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22,
                    'x': 23, 'y': 24, 'z': 25, 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8,
                    'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
                    'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
number_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l',
                    12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w',
                    23: 'x', 24: 'y', 25: 'z'}


def encrypt(key, message):
    # iterate through message
    ciphertext = ""
    for i in range(len(message)):
        # skip spaces
        if message[i] == " ":
            ciphertext += " "
            continue

        # get the characters from the key and the message
        key_letter = key[i % len(key)]
        message_letter = message[i]

        # turn them into numbers from 0 (a) to 25 (z)
        key_number = letter_to_number[key_letter]
        message_number = letter_to_number[message_letter]

        # add the key to the message, loop around if necessary
        ciphertext_number = (key_number + message_number) % 26

        # convert the ciphertext number to a letter
        ciphertext_letter = number_to_letter[ciphertext_number]

        # append it to the cipher text
        ciphertext += ciphertext_letter

    return ciphertext
