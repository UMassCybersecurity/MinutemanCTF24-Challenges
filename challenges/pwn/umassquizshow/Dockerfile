FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install ncat -y

USER 1001

WORKDIR /home/1001

COPY ./static/umass_quiz_show ./
COPY flag.txt ./

EXPOSE 6432

CMD nc -p 6432 -lvke ./umass_quiz_show
