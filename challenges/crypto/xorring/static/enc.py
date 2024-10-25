SECRET_KEY =  bytearray(b"K3YS_4R3_US3D_T0_ENCRyPT_D4T4")

FLAG = bytearray(open("flag.txt","rb").read())

for i in range(0,len(FLAG)):
    FLAG[i] = FLAG[i] ^ SECRET_KEY[i % len(SECRET_KEY)]

print(FLAG)