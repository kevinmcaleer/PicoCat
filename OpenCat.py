# PicoCat
# 31 January 2020
# Kevin McAlee

from machine import Pin, PWM


FEET = ('FRONT_LEFT', 'FRONT_RIGHT', 'BACK_LEFT', 'BACK_RIGHT')

class Servo():
    """ Models a cats foot """
    __name = ""                   # The name of the Foot - Front_Right etc
    __current_angle = 90        # the current angle of the servo
    __transition = "easy_ease"  # the transition type for easing in and out
    __duration = 0.5            # the duration of the transition
    __channel = 0               # the channel of the PWM servo (for PCA9685)
    __pin = 0                   # the pin that the servo is connected to (if not using PCA9685)

    def __init__(self, name=None, pin=None):
        if name is not None:
            print(name)
            self.__name = name
            
        if pin is not None:
            print(pin)
            self.__pin = pin
        pwm = PWM(Pin(self.pin))

    @property
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, value):
        if value < 40:
            self.__pin = value
        else:
            print("Pin value higher than pins available on Pico")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def show(self):
        print(self.__name)

    @property
    def angle(self):
        return self.__current_angle
    
    @angle.setter
    def angle(self, value):
        self.__current_angle = value

class PicoCat():
    name = "PicoCat"
    feet = []
    left_foot = Servo(name=FEET.FRONT_LEFT)
    feet.append(left_foot)

    def __init__(self):
        print("***", self.name, "is Online ***")

cat = PicoCat()
