FROM python:alpine3.19

RUN pip install websockets

# Copy assets needed.
COPY src/app /app
COPY src/flag.txt /app

WORKDIR /app
EXPOSE 6789
#
CMD ["python3","server.py"]