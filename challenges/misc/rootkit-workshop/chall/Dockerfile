FROM ubuntu:24.04 AS build

RUN apt-get update && apt-get install -y build-essential
WORKDIR /build

COPY mod.c mod.c
RUN gcc -shared -fPIC mod.c -o mod.so

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y netcat-traditional wget lsof

RUN echo 'root:aidsovnfjniowrfpeqicnjkdvbkboufQEFKJSB' | chpasswd
RUN echo 'ubuntu:kdlsamvioenlkdsnosacimpwevnslkdvn' | chpasswd

# WORKDIR /home/ubuntu
# RUN wget https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox
# RUN chmod +x busybox

WORKDIR /ctf

COPY ynetd ynetd
COPY entrypoint.sh entrypoint.sh
RUN chmod 700 *

COPY --from=build /build/mod.so mod.so
RUN chmod 755 mod.so

RUN chown root:root *

RUN echo "/ctf/mod.so" > /etc/ld.so.preload
RUN chmod 644 /etc/ld.so.preload

ENTRYPOINT [ "./entrypoint.sh" ]