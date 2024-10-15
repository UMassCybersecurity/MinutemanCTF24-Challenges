FROM docker.io/alpine:3.20.2

USER 1001

ENV FLAG MINUTEMAN{hello}
ENV PASSWORD fldjshfskdfnjksbvjkalsh3kj3vas

COPY ./static/oppenheimers-research.o /bin/ctfmain

EXPOSE 8000

CMD nc -p 8000 -lvke ctfmain