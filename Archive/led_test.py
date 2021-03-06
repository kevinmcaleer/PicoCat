# led_test.py

from machine import Pin, PWM
from time import sleep

led = PWM(Pin(25))
led.freq(1000)

while True:
    for brightness in range(0, 65500, 10):
        led.duty_u16(brightness)
        sleep(0.0000001)
    for brightness in range(65500,0, -10):
        led.duty_u16(brightness)
        sleep(0.0000001)