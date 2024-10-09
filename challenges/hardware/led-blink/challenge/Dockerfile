FROM docker.io/gcc:latest

# Install deps
RUN apt update
RUN apt install libelf-dev ncat -y

# Setup environment
ARG INSTALL_DIR=/usr/src/krusty_krab_heist
RUN mkdir -p ${INSTALL_DIR}
WORKDIR ${INSTALL_DIR}

# Copy project
COPY . .

# Build
RUN ./build.sh

# Clean up
RUN rm -rf ./src
RUN rm -rf ./include
# RUN rm -rf ./lib

EXPOSE 4000

# Run (the k flag keeps the connection alive even after the peer leaves)
CMD ncat -lnvkp 4000 -e ./build/main 