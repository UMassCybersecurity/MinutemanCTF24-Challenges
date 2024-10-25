FROM python:latest

COPY ynetd .
COPY flag.txt .
COPY main.py .

EXPOSE 4444
CMD ./ynetd -p 4444 "python main.py"