FROM python:latest

COPY ynetd .
COPY flag.txt .
COPY main.py .
RUN chmod 755 ynetd

EXPOSE 4447 
CMD ./ynetd -p 4447 "python main.py"