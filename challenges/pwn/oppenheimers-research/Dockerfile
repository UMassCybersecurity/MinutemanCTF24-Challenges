FROM docker.io/alpine:3.20.2

# RUN apk add socat

USER 1001

ENV FLAG MinutemanCTF{hello}
ENV PASSWORD fldjshf^skdfnjksbvjkalsh3kj3vas

COPY ./static/oppenheimers-research.o /bin/ctfmain

EXPOSE 8000

CMD nc -p 8000 -lvke ctfmain