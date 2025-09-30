FROM ubuntu:24.04 AS challenge

RUN apt-get update
RUN apt-get install -y openssh-server python3

# TODO: switch to ubuntu user for ssh?
RUN passwd -d root

WORKDIR /ctf

COPY flag.txt .
COPY main.py .
COPY entrypoint.sh .
COPY spawn-user.sh spawn-user.sh

RUN chmod +x *
RUN chown root:root *
RUN chmod 744 flag.txt

# Set as user shell
RUN usermod --shell /ctf/spawn-user.sh root

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo "PermitRootLogin yes" > /etc/ssh/sshd_config
RUN echo "AllowUsers root" >> /etc/ssh/sshd_config
RUN echo "ClientAliveInterval 3600" >> /etc/ssh/sshd_config
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config

ENTRYPOINT [ "./entrypoint.sh" ]