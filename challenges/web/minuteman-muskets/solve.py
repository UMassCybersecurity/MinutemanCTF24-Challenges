import requests as r 
import json
URL = "http://localhost:4000"
for i in range(0,1000):
    r1 = r.post(f"{URL}/guess", headers= {
        'Content-Type': 'application/json'
    },data=json.dumps({'code':i}))
    print(i)
    if 'correct' in r1.json():
        print(r1.text)
        exit()
print("Could not find correct number.")