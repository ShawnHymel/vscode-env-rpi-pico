# VS Code Docker Environment for Raspberry Pi Pico

WORK IN PROGRESS!!!

TODO:
 - Configure VS Code to launch serial-server.py at same time as container on Run
 - Configure container to auto-connect to serial-server.py (e.g. with socat)
 - Be able to run container (to build) manually and from Dev Containers plugin
 - Verify print debugging from within container
 - Round-trip latency test?
 - Configure VS Code to launch OpenOCD at the same time as container on Debug
 - Configure container to auto-connect to OpenOCD with GDB
 - Verify you can step-through code (inside or outside container?)

## Install Dependencies

 * Install Python (>3.6)
 * Install VS Code
 * Install Docker Desktop


Install Python packages:

```sh
python -m pip install pyserial
```

## Build Docker Container

Run the following command to build the Docker container (from this directory):

```sh
docker build -t env-pico .
```

## Configure VS Code to Build and Debug

TODO

## Manually Interact with Build Environment

As an alternative to using VS Code to interact with the build container, you can perform these actions manually. This allows you to build, flash, and debug without the need for VS Code (or to set up a different editor as your development environment).

### Manually Build and Flash

In a terminal, start the container in interactive mode with the ability to communicate with the host's TCP/UDP services. Note the `--rm` tag--the container will automatically be deleted upon exit.

```sh
docker run --rm -it -v .:/workspace --add-host=host.docker.internal:host-gateway env-pico bash
```

Configure the *blink* example project with CMake and build the project (inside the container):

```
# cd /workspace/
# mkdir -p blink/build/
# cd blink/build
# cmake ..
# make
```

Put your Raspberry Pi Pico into bootloader mode: hold down the *BOOTSEL* button while plugging in the USB cable. Copy the *blink.uf2* file in the *blink/build/* directory to the *RPI-RP2* drive on your computer.

### Serial Debugging

In another terminal, start the serial server, where */serial/dev* is the path to your physical serial port (e.g. *COM4* for Windows, */dev/cu.usbserial-1420* for macOS, */dev/ttyS0* for Linux). This service exposes a port (e.g. 2300) to the local machine sends data to/from the associated physical serial port using the RFC 2217 protocol.

```sh
python serial-server.py -p 2300 COM4
```

Note that you can quit the serial server with *ctrl+c*.

Back in the terminal with the interactive container, start the *socat* client, which connects to the *serial-server.py* application and creates a serial device file named */dev/ttyPico*.

```
# socat pty,link=/dev/ttyPico,raw tcp:host.docker.internal:2300 &
```

*/dev/ttyPico* should be connected to your physical serial port on your host through a TCP/IP connection (thanks to the RFC 2217 protocol). Now, you can use a serial program to communicate directly with the device. The Docker image comes with *minicom*, *picocom*, and *tio*. For example:

```
# tio -b 9600 /dev/ttyPico
```

With the *blink* program, you should see `Blinking!` appear in the console every couple of seconds. Press *ctrl+t, q* to exit *tio*.

### Step-Through Debugging

TODO
