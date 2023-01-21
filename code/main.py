import settings
import machine
import time
from wifi import wifi
import dht


led = machine.Pin("LED", machine.Pin.OUT)
sensor = dht.DHT22(machine.Pin(2)) # For future reference Pin2 is GPIO 2 not pin 2 on the board.

# Have a look at implementing the main entry point
# https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/
try:
    wifi.connect(settings.WIFI['ssid'], settings.WIFI['password'])
except KeyboardInterrupt:
    machine.reset()

print("starting to measure sensor")
while (True):
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    time.sleep(2)

# while (True):
#     led.on()
#     time.sleep(0.5)
#     led.off()
#     time.sleep(0.5)

#TODO: MQTT
# https://github.com/micropython/micropython-lib/tree/master/micropython
# https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html

