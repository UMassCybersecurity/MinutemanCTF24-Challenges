FROM node:alpine
WORKDIR /app
COPY src/package.json .
RUN npm i
COPY src .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]