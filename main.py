import settings
import network
import machine
import time
from code.wifi import wifi


led = machine.Pin("LED", machine.Pin.OUT)

# Have a look at implementing the main entry point
# https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/
try:
    wifi.connect(settings.WIFI['ssid'], settings.WIFI['password'])
except KeyboardInterrupt:
    machine.reset()

#TODO: MQTT
# https://github.com/micropython/micropython-lib/tree/master/micropython
# https://mpython.readthedocs.io/en/master/library/mPython/umqtt.simple.html

