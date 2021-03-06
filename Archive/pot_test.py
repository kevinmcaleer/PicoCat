from machine import Pin, PWM, ADC
import time

print("setting servo")
servo = PWM(Pin(1))

print("Setting up LED")
led = PWM(Pin(25))

print("setting pot")
potentiometer = ADC(26)

print("setting servo frequency")
freq = 50
servo.freq(freq)
led.freq(1000)

while True:
    # print("reading pot")
    pot = potentiometer.read_u16()
    duty = pot
    print('pot ', pot, ' duty:', duty, 'Freq:', freq)
    servo.duty_ns(int(duty))
    led.duty_u16(int(duty))
    time.sleep(0.001)