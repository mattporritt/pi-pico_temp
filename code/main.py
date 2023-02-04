import settings
import machine
import time
from wifi import wifi
import dht
from epaper import epaper
from imggen import imggen
import framebuf
import micropython
import gc

#led = machine.Pin("LED", machine.Pin.OUT)
sensor = dht.DHT22(machine.Pin(2)) # For future reference Pin2 is GPIO 2 not pin 2 on the board.
epd = epaper.EPD_2in13()
epd.init(epd.full_update)
epd.Clear(0xff)  # Clear the paper display

# Have a look at implementing the main entry point
# https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/
try:
    wifi.connect(settings.WIFI['ssid'], settings.WIFI['password'])
except KeyboardInterrupt:
    machine.reset()

# Load the background image
with open('pics/background.pbm', 'rb') as f:
    f.readline() #Magic number
    f.readline()
    f.readline()
    data = bytearray(f.read())

background_buffer = framebuf.FrameBuffer(data, 122, 250, framebuf.MONO_HLSB)
del data
gc.collect()
imggen = imggen.ImageGenerator()

i = 0
while (True):
    # See: https://www.waveshare.com/wiki/Pico-ePaper-2.13#Precautions
    # For rules around use
    if i < 5:
        epd.init(epd.part_update)
    else:
        epd.init(epd.full_update)
        epd.Clear(0xff)  # Clear the paper display

    # Get the DHT22 sensor measurements.
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()

    #print('temp from sensor {}'.format(temp))
    in_temp_buffer = imggen.float_to_image(temp)
    #print(micropython.mem_info())
    background_buffer.blit(in_temp_buffer, 0, 24)
    del in_temp_buffer
    gc.collect()

    epd.fill(0xff)
    epd.blit(background_buffer, 0, 0)

    #epd.text("Temp: {}C".format(temp), 0, 10, 0x00)
    #epd.text("Humidity: {:.0f}% ".format(hum), 0, 30, 0x00)
    if i < 5:
        print('Partial update.')
        epd.displayPartial(epd.buffer)
    else:
        print('Full update')
        epd.display(epd.buffer)
        i = 0
    epd.sleep()

    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    i += 1
    time.sleep(5)

# while (True):
#     led.on()
#     time.sleep(0.5)
#     led.off()
#     time.sleep(0.5)

#TODO: MQTT
# https://github.com/micropython/micropython-lib/tree/master/micropython
# https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html

