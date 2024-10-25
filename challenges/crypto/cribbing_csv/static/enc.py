file = bytearray(open("crib.csv","rb").read())

# Reads 32 bytes from a cryptographically secure random generator
SECRET_KEY = open("/dev/urandom","rb").read(32)

for i in range(0,len(file)):
    file[i] = file[i] ^ SECRET_KEY[i%len(SECRET_KEY)]

open("crib.csv_enc","wb").write(bytes(file))