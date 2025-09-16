FROM ubuntu:24.04 AS instantiator

RUN apt-get update
RUN apt-get install -y docker.io sudo openssh-server

ARG SSH_USER=sshuser
ARG CHALLENGE_USER=root
ARG CHALLENGE_CONTAINER_IMG=challenge

# Create ssh user
RUN adduser ${SSH_USER}
RUN passwd -d ${SSH_USER}

# Allow passwordless sudo for docker
RUN echo "${SSH_USER} ALL=(ALL) NOPASSWD: /usr/bin/docker run -it --rm -u ${CHALLENGE_USER} ${CHALLENGE_CONTAINER_IMG}" > /etc/sudoers.d/docker
RUN chmod 440 /etc/sudoers.d/docker

# Create start script
RUN printf "#!/bin/sh\n\nsudo /usr/bin/docker run -it --rm -u ${CHALLENGE_USER} ${CHALLENGE_CONTAINER_IMG}" > /usr/bin/dsh
RUN chmod +x /usr/bin/dsh

# Set as user shell
RUN usermod --shell /usr/bin/dsh ${SSH_USER}

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo "PermitRootLogin no" > /etc/ssh/sshd_config
RUN echo "AllowUsers ${SSH_USER}" >> /etc/ssh/sshd_config
RUN echo "ClientAliveInterval 3600" >> /etc/ssh/sshd_config
RUN echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config

ENTRYPOINT [ "/usr/sbin/sshd", "-D" ]