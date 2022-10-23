# Pi Pico Temp
A project to measure temp and humidity using a Pi Pico W.
Uses a x temp and humidity sensor and the output is displayed on an y eink display.  Measurements are also sent to a MQTT server

# Set up and install
The following instructions are a rough guide on how to install the code and run it on the Pi Pico.

Instructions assume the host machine is using MacOS.

## Get the code
Clone this repository to a directory on your host machine:

`git clone git@github.com:mattporritt/pi-pico_temp.git`

## Prepare the Pi Pico W
Before we can load the project onto the Pi Pico W some setup of the Pi device itself needs to be completed. Full documentation can be found here: https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
A shortcut guide is below:
* Download the UF2 file from here: https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2
* Push and hold the BOOTSEL button and plug a USB cable from your computer into the Pi Pico W
* Release the BOOTSEL button after your Pico is connected.
* The Pico will mount as a Mass Storage Device called RPI-RP2.
* Drag and drop the MicroPython UF2 file onto the RPI-RP2 volume. 
* Your Pico will reboot. You are now running MicroPython.
* Keep the Pi Pico connect via USB.

## Pycharm Setup
If we haven’t developed for the Pi Pico on Pycharm before the Micro Python Pycharm plugin needs to be installed.
To do this:
* Launch pycharm
* Select plugins from the launch menu
* Search for "MicroPython" in the marketplace
* Click install
* Follow prompts then restart IDE
* Finally open the location you downloaded the repository as a new Python project from existing sources.

Next we need to configure Pycharm to connect to the Pi Pico W so the code can be loaded.
First we need to find the address of the USB Modem of the Pi Pico.
To do this run the following command:

`ls -ls /dev/cu.*`

We're looking for a response that looks like: `/dev/cu.usbmodem401101`

Once we have the modem location we can configure PyCharm. To do this:
* Go to PyCharm Preferences > Languages and Frameworks & > MicroPython
* Check: Enable MicroPython support
* Change device type to: Raspberry Pi Pico
* Set the device path to the result of the above `ls` command

## Loading the Pi Pico W with the project code
TODO


