file = bytearray(open("static/crib.csv_enc","rb").read())

CRIB = bytearray(open("static/sample_crib.csv","rb").readline())
SECRET_KEY = []

for i in range(0,32):
    SECRET_KEY.append(file[i] ^ CRIB[i])

SECRET_KEY = bytearray(SECRET_KEY)


for i in range(0,len(file)):
    file[i] = file[i] ^ SECRET_KEY[i%len(SECRET_KEY)]

print(file.decode())