import requests as r 

URL = "http://localhost:4444"

r1 = r.post(f"{URL}?best_category=web_of_course",headers = {
    'Cookie':'best_ctf=minuteman_ctf',
    'Content-Type':'application/json'
},json={'deservesFlag':True})
print(r1.text)