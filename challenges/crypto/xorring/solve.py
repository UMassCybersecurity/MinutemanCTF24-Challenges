SECRET_KEY =  bytearray(b"K3YS_4R3_US3D_T0_ENCRyPT_D4T4")

ENC_FLAG = open("static/encrypted_flag.txt","rb").read()
FLAG = ""

for i in range(0,len(ENC_FLAG)):
    FLAG += chr(ENC_FLAG[i] ^ SECRET_KEY[i % len(SECRET_KEY)])

print(FLAG)