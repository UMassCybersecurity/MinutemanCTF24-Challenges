FROM node:22-alpine
COPY entrypoint.sh /entrypoint.sh
RUN apk add chromium
RUN chmod +x /entrypoint.sh
WORKDIR app
COPY app/package.json package.json
RUN npm i 
COPY app .
USER node
ENTRYPOINT /entrypoint.sh