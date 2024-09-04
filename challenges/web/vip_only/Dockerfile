# Use the official Node.js image as base
FROM node:18

# Set the working directory in the container
WORKDIR /src

# Copy package.json and package-lock.json to the container
COPY package.json .

# Install app dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY ./src/* .

# Expose the port on which the Node.js app will run
EXPOSE 3000

# Command to start the Node.js app
CMD ["node", "index.js"]
