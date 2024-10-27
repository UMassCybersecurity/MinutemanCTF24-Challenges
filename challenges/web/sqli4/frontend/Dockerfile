FROM python:3.13-rc-slim as builder

WORKDIR /code
COPY requirements.txt /code
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP frontend.py
ENV FLASK_RUN_PORT 1337
ENV FLASK_RUN_HOST 0.0.0.0
ENV PYTHONUNBUFFERED=1

EXPOSE 1337

CMD ["flask", "run", "--port", "1337"]