FROM python:alpine3.19
RUN pip install flask gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY src /app
ENV FLAG UMASS{CR4CK3D_TH3_C0D3_T0_Th3_MUSK3TS}
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]