from machine import Pin, PWM, ADC
from time import sleep

servo = PWM(Pin(0))

freq = 50
servo.freq(freq)

duty_cycles = [7000, 1000, 9000, 3000, 4500]

while True:
    for duty in duty_cycles:
        servo.duty_u16(duty)
    # led.duty_u16(int(duty))
        print(duty)
        sleep(2)