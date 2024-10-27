
flag = "MINUTEMAN{TEST}"

super_secret_key = 42

while super_secret_key % 11 != 0:
    super_secret_key = (2*super_secret_key) + 1

while super_secret_key > 100:
    super_secret_key //= 10
    
flag = flag.replace("MINUTEMAN", "HOURGUY")

flag = flag[super_secret_key:] + flag[:super_secret_key]

splitFlag = flag.split("_")
flag = ":".join(reversed(splitFlag))

flag = "^".join(flag)

flag = flag[::-1]

print(flag)
# with open("encoded.txt", "w") as f:
#     f.write(flag)
