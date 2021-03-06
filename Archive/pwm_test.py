from machine import PWM, Pin
from time import sleep

servo = PWM(Pin(0))

servo.freq(50)
MAX_DUTY = 9000
MIN_DUTY = 1000
duty = MIN_DUTY

direction = 1
while True:
    for _ in range(1024):
        duty += direction
        if duty > MAX_DUTY:
            duty = MAX_DUTY
            direction = -direction
        elif duty < MIN_DUTY:
            duty = MIN_DUTY
            direction = -direction
        servo.duty_u16(duty)
        # print(duty)
        # sleep(0.00001)


