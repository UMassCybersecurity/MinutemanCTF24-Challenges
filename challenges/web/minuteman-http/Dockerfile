FROM python:alpine3.19
RUN pip install flask gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY src /app
ENTRYPOINT ["/entrypoint.sh"]
