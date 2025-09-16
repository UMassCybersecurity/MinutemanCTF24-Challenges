FROM ubuntu:24.04 AS build

RUN apt-get update
RUN apt-get install -y build-essential
WORKDIR /build

COPY mod.c mod.c
RUN gcc -shared -fPIC -g mod.c -o mod.so


FROM ubuntu:24.04 AS challenge

RUN apt-get update
RUN apt-get install -y netcat-traditional wget lsof openssh-server

# TODO: switch to ubuntu user for ssh?
RUN passwd -d root

WORKDIR /ctf

COPY ynetd ynetd
COPY entrypoint.sh entrypoint.sh
RUN chmod 700 *

COPY --from=build /build/mod.so mod.so
RUN chmod 755 mod.so

COPY spawn-user.sh spawn-user.sh
RUN chmod +x spawn-user.sh

RUN chown root:root *

RUN echo "/ctf/mod.so" > /etc/ld.so.preload
RUN chmod 644 /etc/ld.so.preload

# Set as user shell
RUN usermod --shell /ctf/spawn-user.sh root

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo "PermitRootLogin yes" > /etc/ssh/sshd_config
RUN echo "AllowUsers root" >> /etc/ssh/sshd_config
RUN echo "ClientAliveInterval 3600" >> /etc/ssh/sshd_config
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config

ENTRYPOINT [ "./entrypoint.sh" ]