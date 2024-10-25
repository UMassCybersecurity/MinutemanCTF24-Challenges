difficulty: warmup/easy

description: TODO

hints: 
1) How can you see files inside the docker container?

After building, you can spawn a shell and `find` the flag
```
docker exec -it <id> /bin/bash
cd / 
various ways to find finds:
find . -name flag.txt 2>/dev/null && cat /root/flag.txt
grep -r "UMASS" . 2>/dev/null
```

it will be in `/root/flag.txt`

flag: `UMASS{h1DDen_1N_7hE_con741nER_u1S3UR1r}`