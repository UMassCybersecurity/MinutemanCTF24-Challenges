difficulty: medium/hard

description: TODO

hints:
1) you'll have to find out what files where added and removed when building the container
2) The last layer removes a file. How can you find the secret?
3) one tool that might help is [dive](https://github.com/wagoodman/dive)
4) chall inspiration: https://danaepp.com/finding-api-secrets-in-hidden-layers-within-docker-containers

Look through the image layers to see that `/root/flag2.txt` is removed on the last layer:
[dockerhub](https://hub.docker.com/layers/atch2203/docker-challs/latest/images/sha256-dfda9d3721bfe3874e4fcf523672a8f0406f7a43c0adbdddf3ec914357440070?context=repo)
or
`docker history <id>`

Now we look through the docker vm overlay2 folder (see article for how it works):
```
docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh
# cd /var/lib/docker/overlay2
# find . -name flag2.txt 2>/dev/null
# find . -name flag2.txt -exec cat {} \; 2>/dev/null
# find . -name flag2.txt -exec echo {} \; -exec cat {} \; 2>/dev/null
```

Alternatively, follow the article:
1) run `dive <id>` and look through the layers to find where `root/flag2.txt` was added (filter out added files only)
2) run `docker image inspect <id>` and go to the section 
3) count the layers from the bottom (in this case it's 2nd from bottom=first in Lowerdir list)
4) like the other solution go to doverk vm overlay2 
```bash
docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh
# cd /var/lib/docker/overlay2
```
5) go to that folder and run `cat root/flag2.txt`

flag: `UMASS{C0n741n3r5_4R3_l1K3_0N10n2_gax7ESEa}`