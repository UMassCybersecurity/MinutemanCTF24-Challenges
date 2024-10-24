FROM python:alpine3.19

RUN pip install websockets

# Copy assets needed.
COPY app /app
COPY flag.txt /app

WORKDIR /app
EXPOSE 6789
#
CMD ["python3","server.py"]