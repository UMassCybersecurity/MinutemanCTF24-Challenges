FROM python:latest

COPY ynetd .
COPY flag.txt .
COPY public_keys.txt .
COPY main.py .

RUN pip3 install pycryptodome

EXPOSE 4444
CMD ./ynetd -p 4444 "python main.py"