FROM python:latest

COPY ynetd .
COPY flag.txt .
COPY public_keys.txt .
COPY main.py .
RUN chmod 755 ynetd

RUN pip3 install pycryptodome

EXPOSE 4446 
CMD ./ynetd -p 4446 "python main.py"