ENC_MAPPING = {
    "0": "\u02ea",
    "1": "\u032b",
    "2": "\u022a",
    "3": "\u01bd",
    "4": "\u0355",
    "5": "\u0325",
    "6": "\u035a",
    "7": "\u00ae",
    "8": "~",
    "9": "\u0317",
    "a": "\u018a",
    "b": "\u01ad",
    "c": "\u00f9",
    "d": "\u02a2",
    "e": "\u0164",
    "f": "\u034d",
    "g": "\u035a",
    "h": "\u0392",
    "i": "R",
    "j": "\u0130",
    "k": "\u019e",
    "l": "\u028b",
    "m": "\u03d1",
    "n": "\u00ab",
    "o": "\u0332",
    "p": "l",
    "q": "\u00ad",
    "r": "\u0265",
    "s": "\u0135",
    "t": "\u019a",
    "u": "\u0176",
    "v": "\u0321",
    "w": "\u0236",
    "x": "\u01e5",
    "y": "\u00e0",
    "z": "\u00cb",
    "A": "\u014c",
    "B": "\u00de",
    "C": "\u0254",
    "D": "\u036f",
    "E": "\u0240",
    "F": "\u02ff",
    "G": "\u03d6",
    "H": "\u038a",
    "I": "\u0277",
    "J": "\u008f",
    "K": "9",
    "L": "\u01fd",
    "M": "\u02a7",
    "N": "\u021a",
    "O": "\u00d8",
    "P": "\u0230",
    "Q": "\u0299",
    "R": "\u0306",
    "S": "\u03dd",
    "T": "\u0269",
    "U": "\u026d",
    "V": "\u02e5",
    "W": "\u033e",
    "X": "\u0329",
    "Y": "\u0270",
    "Z": "\u0362",
    "!": "\u034f",
    "\"": "\u03da",
    "#": "\u020e",
    "$": "\u00c9",
    "%": "\u011f",
    "&": "\u010b",
    "'": "\u00e6",
    "(": "\u0393",
    ")": "\u030c",
    "*": "\u0278",
    "+": "\u00cf",
    ",": "\u01f5",
    "-": "\u02bd",
    ".": "n",
    "/": "\u009d",
    ":": "\u0090",
    ";": "\u013f",
    "<": "\u011c",
    "=": "\u015c",
    ">": "\u03c7",
    "?": "\u01dc",
    "@": "\u02b5",
    "[": "\u0365",
    "\\": "\u03a2",
    "]": "\u01df",
    "^": "}",
    "_": "\u0261",
    "`": "\u00d1",
    "{": "\u0315",
    "|": "\u0353",
    "}": "g",
    "~": "\u0106",
    " ": "\u00db",
    "\t": "\u025a",
    "\n": "\u0184",
    "\r": "t",
    "\u000b": "\u00d0",
    "\f": "\u0243"
}

import random
import json

for key in ENC_MAPPING:
    ENC_MAPPING[key] = chr(random.randint(21,1000))

ENC_FLAG = list("MINUTEMAN{TH3_S3Cr3T_W4S_H1dd3N_But_N0t_w3ll_3n0ugh}")

for i in range(len(ENC_FLAG)):
    char = ENC_FLAG[i]
    ENC_FLAG[i] = ENC_MAPPING[char]

ENC_FLAG = "".join(ENC_FLAG)

print(ENC_MAPPING)

print(ENC_FLAG)

DEC_MAPPING = {}
for key in ENC_MAPPING:
    DEC_MAPPING[ENC_MAPPING[key]] = key

FLAG = ""
for x in ENC_FLAG:
    FLAG += DEC_MAPPING[x]

print("".join(FLAG))