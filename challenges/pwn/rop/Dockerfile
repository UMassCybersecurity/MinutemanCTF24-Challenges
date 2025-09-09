FROM ubuntu:24.04

RUN echo "root:root0789dsklfj90w3423w5298204e09sdfh" | chpasswd

WORKDIR /home/ctf

RUN useradd -d /home/ctf/ ctf
RUN echo "ctf:ctf43533241375f98gd9f8gds0f989089dzxdf0v8sd" | chpasswd

COPY static/chatbot .
COPY ynetd .
COPY flag.txt .

RUN chmod -R 555 /home/ctf
RUN chown -R root:root /home/ctf

# TODO port
EXPOSE 4445 
CMD ./ynetd -p 4445 "su - ctf -c ./chatbot"