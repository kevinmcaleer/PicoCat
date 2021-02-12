# Range Finder
# PicoCat 2021
#define echoPin 8 
#define trigPin 7 

from machine import Pin
from time import sleep_us, ticks_us

class Range_Finder():

    duration = 0
    distance = 0

    def __init__(self, echo_pin, trigger_pin):
        # Initialise the Range Finder
        self.__echo_pin = Pin(echo_pin, Pin.IN)
        self.__trigger_pin = Pin(trigger_pin, Pin.OUT)
        # print("Range Finder Enabled")
    
    def ping(self):
        # print("Ping...")
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
        
        # print(elapsed_micros)
        # print("cm: ", (elapsed_micros * 0.343) /2 ) # /!\ have to check if this calc is ok.
        # self.duration = elapsed_micros-start / 29 / 2 # in cm
        # sleep_us(1000)
        
        # distance in mm
        self.distance = (elapsed_micros * 0.343) /2
        return self.distance 

while True:
    t = Range_Finder(echo_pin=2, trigger_pin=3)
    print("distance is ", round(t.ping(),1))