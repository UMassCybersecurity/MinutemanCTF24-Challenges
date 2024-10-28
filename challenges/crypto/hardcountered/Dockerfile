FROM python:latest

COPY ynetd .
COPY flag.txt .
COPY main.py .

RUN pip3 install pycryptodome
RUN chmod 755 ynetd

EXPOSE 4444
CMD ./ynetd -p 4444 "python main.py"