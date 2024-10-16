FROM ubuntu:24.04

RUN echo "root:root07896789340275098236489127" | chpasswd

WORKDIR /home/ctf

RUN useradd -d /home/ctf/ ctf
RUN echo "ctf:ctf4353254387438958902" | chpasswd

COPY static/oppenheimers-research .
COPY ynetd .

RUN chmod 755 oppenheimers-research
RUN chmod 755 ynetd

RUN chown -R root:root /home/ctf

USER ctf

ENV FLAG MINUTEMAN{COnfIdenTiAL_r3sEaRch}
ENV PASSWORD 809834*FDUOsdiofu&23

# TODO port
EXPOSE 4444
CMD ./ynetd -p 4444 ./oppenheimers-research