FROM python:3.10-slim-bookworm

RUN useradd -ms /bin/bash newuser
USER newuser
RUN pip3 install flask
COPY ./src/ /src
COPY ./flag12490.txt /src/flag12490.txt
WORKDIR "/src"

EXPOSE 9000
CMD ["python3", "./main.py"]