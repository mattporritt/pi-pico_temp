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
    intemp = sensor.temperature()
    inhum = sensor.humidity()

    # TODO: MQTT
    # https://github.com/micropython/micropython-lib/tree/master/micropython
    # https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html
    outtemp = intemp + 1
    outhum = inhum + 1
    outuv = 13
    outwind = 33.3
    outpressure = 1008.3

    in_temp = imggen.float_to_image(intemp, 1, 'lg')
    background_buffer.blit(in_temp['buffer'], 0, 24)
    in_temp_offset = in_temp['offset']
    del in_temp
    gc.collect()

    in_temp_sym = imggen.get_sym_buffer('sym_degc')
    background_buffer.blit(in_temp_sym, in_temp_offset, 24)
    del in_temp_sym
    gc.collect()

    in_humid = imggen.float_to_image(inhum, 0, 'lg')
    background_buffer.blit(in_humid['buffer'], 0, 55)
    in_humid_offset = in_humid['offset']
    del in_humid
    gc.collect()

    in_humid_sym = imggen.get_sym_buffer('sym_hum')
    background_buffer.blit(in_humid_sym, in_humid_offset, 55)
    del in_humid_sym
    gc.collect()

    out_temp = imggen.float_to_image(outtemp, 1, 'lg')
    background_buffer.blit(out_temp['buffer'], 0, 112)
    out_temp_offset = out_temp['offset']
    del out_temp
    gc.collect()

    out_temp_sym = imggen.get_sym_buffer('sym_degc')
    background_buffer.blit(out_temp_sym, out_temp_offset, 112)
    del out_temp_sym
    gc.collect()

    out_humid = imggen.float_to_image(outhum, 0, 'lg')
    background_buffer.blit(out_humid['buffer'], 0, 144)
    out_humid_offset = out_humid['offset']
    del out_humid
    gc.collect()

    out_humid_sym = imggen.get_sym_buffer('sym_hum')
    background_buffer.blit(out_humid_sym, out_humid_offset, 144)
    del out_humid_sym
    gc.collect()

    out_uv = imggen.float_to_image(outuv, 0, 'sml')
    background_buffer.blit(out_uv['buffer'], 24, 178)
    out_uv_offset = out_uv['offset'] + 26
    del out_uv
    gc.collect()

    out_uv_sym = imggen.get_sym_buffer('sym_uv')
    background_buffer.blit(out_uv_sym, out_uv_offset, 178)
    del out_uv_sym
    gc.collect()

    out_wind = imggen.float_to_image(outwind, 0, 'sml')
    background_buffer.blit(out_wind['buffer'], 24, 204)
    out_wind_offset = out_wind['offset'] + 26
    del out_wind
    gc.collect()

    out_wind_sym = imggen.get_sym_buffer('sym_kmh')
    background_buffer.blit(out_wind_sym, out_wind_offset, 204)
    del out_wind_sym
    gc.collect()

    out_pressure = imggen.float_to_image(outpressure, 0, 'sml')
    background_buffer.blit(out_pressure['buffer'], 24, 229)
    out_pressure_offset = out_pressure['offset'] + 26
    del out_pressure
    gc.collect()

    out_pressure_sym = imggen.get_sym_buffer('sym_hpa')
    background_buffer.blit(out_pressure_sym, out_pressure_offset, 229)
    del out_pressure_sym
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

    print("Temperature: {}°C   Humidity: {:.0f}% ".format(intemp, inhum))
    i += 1
    gc.collect()
    time.sleep(60)
