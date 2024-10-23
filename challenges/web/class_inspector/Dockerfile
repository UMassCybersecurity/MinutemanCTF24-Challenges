FROM python:3.10-slim-bookworm

RUN useradd -ms /bin/bash newuser
USER newuser
RUN pip3 install flask
COPY ./src/ /src
COPY ./flag934UMASS.txt /src/flag934UMASS.txt
WORKDIR "/src"

EXPOSE 8080
CMD ["python3", "./main.py"]