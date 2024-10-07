# Base image
FROM ubuntu:24.04

# Install toolchain
RUN \
    # Set up directories
    mkdir -p /toolchain/ && \
    mkdir -p /workspace/ && \
    # Don't prompt the user during installation
    export DEBIAN_FRONTEND=noninteractive && \
    # Install dependencies
    apt-get update && \
    apt-get install -y wget python3 pkg-config socat minicom picocom tio && \
    # Install Raspberry Pi Pico toolchain (ignore "sudo" in script)
    cd /toolchain/ && \
    wget https://raw.githubusercontent.com/raspberrypi/pico-setup/4567073441c6ef298988baf49a8700f507c3b5a0/pico_setup.sh && \
    chmod +x pico_setup.sh && \
    sed 's/\bsudo\b//g' pico_setup.sh | bash

# Default entrypoint
ENTRYPOINT ["/bin/sh", "-c"]