# Base image
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    wget \
    python3 \
    python3-pip \
    pkg-config \
    socat \
    minicom \
    picocom \
    tio

# Install toolchain
RUN \
    # Set up directories
    mkdir -p /toolchain/ && \
    mkdir -p /workspace/ && \
    # Don't prompt the user during installation
    export DEBIAN_FRONTEND=noninteractive && \
    # Install Raspberry Pi Pico toolchain (ignore "sudo" in script)
    cd /toolchain/ && \
    wget https://raw.githubusercontent.com/raspberrypi/pico-setup/4567073441c6ef298988baf49a8700f507c3b5a0/pico_setup.sh && \
    chmod +x pico_setup.sh && \
    sed 's/\bsudo\b//g' pico_setup.sh | bash

# Set environment variables
ENV PICO_EXTRAS_PATH=/toolchain/pico/pico-extras
ENV PICO_SDK_PATH=/toolchain/pico/pico-sdk
ENV PICO_PLAYGROUND_PATH=/toolchain/pico/pico-playground
ENV PICO_EXAMPLES_PATH=/toolchain/pico/pico-examples

# Default entrypoint
ENTRYPOINT ["/bin/sh", "-c"]