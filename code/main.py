import settings
import machine
import time
from wifi import wifi
import dht
from epaper import epaper


led = machine.Pin("LED", machine.Pin.OUT)
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

    epd.fill(0xff)
    epd.text("Temp: {}C".format(temp), 0, 10, 0x00)
    epd.text("Humidity: {:.0f}% ".format(hum), 0, 30, 0x00)

    if i < 5:
        epd.displayPartial(epd.buffer)
    else:
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

