FROM docker.io/python

RUN apt update -y && apt install cmake -y

WORKDIR /home/ctf

# Add user and passwds
RUN echo "root:root0789678934027509823648899127" | chpasswd
RUN useradd -d /home/ctf/ ctf
RUN echo "ctf:ctf4353254387438958908902" | chpasswd

# Install pip libs
COPY server/requirements.txt server/
RUN pip3 install -r server/requirements.txt

# Build sim
COPY sim ./sim
RUN mkdir sim/build && cd sim/build && cmake .. && make

# Copy server
COPY server ./server

RUN chown -R root:root /home/ctf
RUN chown ctf:ctf /home/ctf/server/uploads

USER ctf
WORKDIR /home/ctf/server

CMD gunicorn -w 4 -b :8000 'server:app'