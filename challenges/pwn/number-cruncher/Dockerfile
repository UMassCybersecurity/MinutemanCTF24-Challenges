FROM ubuntu:24.04

RUN apt-get update && apt-get install -y socat

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY number_cruncher .
COPY ynetd .

RUN chmod 755 number_cruncher
RUN chmod 755 ynetd

RUN echo "UMASS{l3t_th3_f1n1t3_l4rg3_0v3rfl0w}" > flag.txt
RUN chown root:ctf flag.txt
RUN chmod 440 flag.txt

RUN chown -R root:root /home/ctf

# USER ctf
EXPOSE 7878

CMD ./ynetd -p 7878 ./number_cruncher