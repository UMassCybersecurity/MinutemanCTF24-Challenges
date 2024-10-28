FROM docker.io/alpine:3.20.2

RUN apk add libc6-compat

USER 1001

WORKDIR /home/1001

COPY ./static/echo360 ./
COPY flag.txt ./

EXPOSE 8787

CMD nc -p 8787 -lvke ./echo360