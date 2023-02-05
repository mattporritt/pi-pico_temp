import network
import time


class Wifi:
    wlan = None
    ssid = ''

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self, ssid, password):
        self.wlan.connect(ssid, password)
        while not self.wlan.isconnected():
            print('Waiting for connection...')
            time.sleep(1)
        self.ssid = ssid
        print(self.wlan.ifconfig())
        #TODO: make it more like this: https://how2electronics.com/getting-started-with-raspberry-pi-pico-w-using-micropython/

    def getStrength(self) -> int:
        signal = -100
        for ap in self.wlan.scan():
            if ap[0].decode() == self.ssid:
                signal = ap[3]

        return signal
