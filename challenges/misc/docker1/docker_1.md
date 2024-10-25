difficulty: warmup

description: TODO

hints:
1) search up `docker run container from dockerfile`
2) The three most popular answers are missing an important point: you need to expose port 80 from the container to the host.

```
docker build . -t <name>
docker run -p80:80 <id>

docker run --name <container_name> -p80:80 -d <id>
```

flag: `UMASS{Ju5t_D0ck3R_8uILd_anD_run_OeLRuxbQ}`
