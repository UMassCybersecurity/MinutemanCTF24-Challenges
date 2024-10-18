FROM python:alpine3.19

RUN pip install websocket

# Copy assets needed.
COPY server.py /server.py
RUN chmod +x /server.py
COPY flag.txt /flag.txt

#
ENTRYPOINT ["/entrypoint.sh"]