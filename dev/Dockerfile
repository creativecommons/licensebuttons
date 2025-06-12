# https://docs.docker.com/engine/reference/builder/

# https://hub.docker.com/_/debian
FROM debian:bookworm-slim

# Configure apt not to prompt during docker build
ARG DEBIAN_FRONTEND=noninteractive

# Configure apt to avoid installing recommended and suggested packages
RUN apt-config dump \
    | grep -E '^APT::Install-(Recommends|Suggests)' \
    | sed -e's/1/0/' \
    | tee /etc/apt/apt.conf.d/99no-recommends-no-suggests

# Resynchronize the package index and install packages
# https://docs.docker.com/build/building/best-practices/#apt-get
RUN apt-get update && apt-get install -y \
        curl \
        git \
        gir1.2-pango-1.0 \
        libnginx-mod-http-fancyindex \
        nginx-light \
        python3-gi-cairo \
        tree \
    && rm -rf /var/lib/apt/lists/*
