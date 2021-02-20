# Range Finder
# PicoCat 2021

from machine import Pin
from time import sleep_us, ticks_us


class Range_Finder():

    duration = 0
    distance = 0

    def __init__(self, echo_pin, trigger_pin):

        self.__echo_pin = Pin(echo_pin, Pin.IN)
        self.__trigger_pin = Pin(trigger_pin, Pin.OUT)


    def ping(self):
        self.__trigger_pin.low()
        sleep_us(2)

        self.__trigger_pin.high()
        sleep_us(5)
        self.__trigger_pin.low()
        signal_on = 0
        signal_off = 0
        while self.__echo_pin.value() == 0:
            signal_off = ticks_us()
        while self.__echo_pin.value() == 1:
            signal_on = ticks_us()

        elapsed_time =  signal_on - signal_off
        self.duration = elapsed_time
        self.distance = (elapsed_time * 0.343) / 2
        return self.distance / 10

while True:
    t = Range_Finder(echo_pin=2, trigger_pin=3) 
    print("distance is: ", round(t.ping(),1)) 


