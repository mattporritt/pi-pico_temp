import sys

import settings
import machine
import time
from wifi import wifi
import dht
from epaper import epaper
from imggen import imggen
import framebuf
import gc

sensor = dht.DHT22(machine.Pin(2)) # For future reference Pin2 is GPIO 2 not pin 2 on the board.
sensor.measure()
time.sleep(10)

wifi.connect(settings.WIFI['ssid'], settings.WIFI['password'])

# Have a look at implementing the main entry point
# https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/
epd = epaper.EPD_2in13()
epd.init(epd.full_update)
epd.Clear(0xff)  # Clear the paper display

# Load the background image
try:
    with open('pics/background.pbm', 'rb') as f:
        f.readline() #Magic number
        f.readline()
        f.readline()
        data = bytearray(f.read())
except EnvironmentError:
    sys.exit()

background_buffer = framebuf.FrameBuffer(data, 122, 250, framebuf.MONO_HLSB)
del data
gc.collect()

imggen = imggen.ImageGenerator()
i = 0
while (True):
    # See: https://www.waveshare.com/wiki/Pico-ePaper-2.13#Precautions
    # For rules around use
    if i < 10:
        epd.init(epd.part_update)
    else:
        epd.init(epd.full_update)
        epd.Clear(0xff)  # Clear the paper display

    # Get the DHT22 sensor measurements.
    sensor.measure()
    time.sleep_ms(100)
    temp = sensor.temperature()
    hum = sensor.humidity()

    in_temp = imggen.float_to_image(temp, 1, 'lg')
    background_buffer.blit(in_temp['buffer'], 0, 24)
    in_temp_offset = in_temp['offset']
    del in_temp
    gc.collect()

    in_temp_sym = imggen.get_sym_buffer('sym_degc')
    background_buffer.blit(in_temp_sym, in_temp_offset, 24)
    del in_temp_sym
    gc.collect()

    in_humid = imggen.float_to_image(hum, 0, 'lg')
    background_buffer.blit(in_humid['buffer'], 0, 55)
    in_humid_offset = in_humid['offset']
    del in_humid
    gc.collect()

    in_humid_sym = imggen.get_sym_buffer('sym_hum')
    background_buffer.blit(in_humid_sym, in_humid_offset, 55)
    del in_humid_sym
    gc.collect()

    epd.fill(0xff)
    epd.blit(background_buffer, 0, 0)

    if i < 10:
        print('Partial update.')
        epd.displayPartial(epd.buffer)
    else:
        print('Full update')
        epd.display(epd.buffer)
        i = 0
    epd.sleep()

    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    i += 1
    time.sleep(60)

#TODO: MQTT
# https://github.com/micropython/micropython-lib/tree/master/micropython
# https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html

