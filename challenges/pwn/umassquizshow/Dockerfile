FROM docker.io/alpine:3.20.2

RUN apk add libc6-compat

USER 1001

WORKDIR /home/1001

COPY ./static/umass_quiz_show ./
COPY flag.txt ./

EXPOSE 6432

CMD nc -p 6432 -lvke ./echo360
