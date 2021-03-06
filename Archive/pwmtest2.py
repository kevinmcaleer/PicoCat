from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(0))
servo.freq(50)

while True:
    servo.duty_u16(7000)
    sleep(2)
    servo.duty_u16(3000)
    sleep(2)
    servo.deinit()