FROM node:18-slim

WORKDIR /SCAV

CMD ["cd", "src"]

COPY src/package.json .

RUN npm i

COPY src/. .

CMD ["node", "./app.js"]
