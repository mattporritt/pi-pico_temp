import settings
import network
import machine
import time
from code.wifi import wifi


led = machine.Pin("LED", machine.Pin.OUT)


try:
    wifi.connect(settings.WIFI['ssid'], settings.WIFI['password'])
except KeyboardInterrupt:
    machine.reset()
