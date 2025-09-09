import requests as r 

URL = "http://localhost:4444"

r1 = r.post(f"{URL}?number_one=in_student_dining",headers = {
    'Cookie':'mascot=sam_the_minuteman',
    'Content-Type':'application/json'
},json={'deservesFlag':True})
print(r1.text)