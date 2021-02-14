# Range Finder
# PicoCat 2021

# Note on a Pico the Range finder needs an input voltage of 5v, but a voltage divider across the returning Echo pin to make sure its only 3.3v
# 1 1k and 2k resistor should achieve this


from machine import Pin
from time import sleep_us, ticks_us

class Range_Finder():

    duration = 0
    distance = 0

    def __init__(self, echo_pin, trigger_pin):
        # Initialise the Range Finder
        self.__echo_pin = Pin(echo_pin, Pin.IN)
        self.__trigger_pin = Pin(trigger_pin, Pin.OUT)
    
    def ping(self):
        self.__trigger_pin.low()
        sleep_us(2)
        
        self.__trigger_pin.high()
        sleep_us(5)
        self.__trigger_pin.low()
        signalon = 0
        signaloff = 0
        while self.__echo_pin.value() == 0:
            signaloff = ticks_us()
        while self.__echo_pin.value() == 1:
            signalon = ticks_us()
        elapsed_micros = signalon - signaloff
        self.duration = elapsed_micros
        self.distance = (elapsed_micros * 0.343) /2
        return self.distance 

while True:
    t = Range_Finder(echo_pin=2, trigger_pin=3)
    print("distance is ", round(t.ping(),1))