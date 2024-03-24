import network
from time import sleep
from machine import Pin
led = Pin(2, Pin.OUT)
led.value(0)
def disconnect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.disconnect()
def connectTo(ssid, password):
    disconnect()
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.scan()
    i = 20
    station.connect(ssid, password)
    while (i>0) and (station.isconnected() == False):
		print("connecting to " + ssid + "   "+str(i))
		i=i-1
		led.value(not led.value())
		try:
			station.connect(ssid, password)
			sleep(0.5)
		except :
			sleep(0.5)
        
    if station.isconnected() == True:
        print("connected to network " + ssid)
        ip = station.ifconfig()
        print("your IP: " +str(ip) )
        led.value(0)
        for i in range(8):
			led.value(not led.value())
			sleep(0.1)
    else:
        print("we can't connect to network. please check!")
        led.value(1)
        while True :
			sleep(1)
def checkConnect():
	station = network.WLAN(network.STA_IF)
	return station.isconnected()
