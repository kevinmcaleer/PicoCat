# PicoCat
# 31 January 2020
# Kevin McAlee

from machine import Pin, PWM
from time import sleep, time

class Limbs():
    """
    setup legs and feet to correspond to the correct channel
    """
    FRONT_LEFT = 0
    FRONT_RIGHT = 1
    BACK_LEFT = 2
    BACK_RIGHT = 3
    TAIL = 4
    NECK = 5
    HEAD = 6


def map(x, in_min, in_max, out_min, out_max):
    # if x == 0:
    #     x = 1
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


class Servo():
    """ Models a cats foot """
    __name = ""                   # The name of the Foot - Front_Right etc
    __current_angle = 90        # the current angle of the servo
    __transition = "easy_ease"  # the transition type for easing in and out
    __duration = 0.5            # the duration of the transition
    __channel = 0               # the channel of the PWM servo (for PCA9685)
    __pin = 0                   # the pin that the servo is connected to (if not using PCA9685)
    __max_angle = 180
    __min_angle = 0

    def __init__(self, name=None, pin=None):
        if name is not None:
            print(name)
            self.__name = name
            
        if pin is not None:
            print(pin)
            self.__pin = pin
        self.__pwm = PWM(Pin(self.__pin))
        self.__pwm.freq(1000)

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
        print("Name: ", self.name)
        print("Pin: ", self.pin)
        print("Current Angle:", self.angle) 

    @property
    def angle(self):
        return self.__current_angle
    
    @angle.setter
    def angle(self, value):
        if (value >= 0) and (value <= 180):
            self.__current_angle = value

            # map values - degrees to duty
            my_angle = map(value, 0, 180, 0, 65025)
            self.__pwm.duty_u16(my_angle)
            sleep(0.0001)
        else:
            print("Angle value less than 0 or greater than 180", value)


    @property
    def max_angle(self):
        return self.__max_angle

    @max_angle.setter
    def max_angle(self, value):
        self.__max_angle = value

    @property
    def min_angle(self):
        return self.__min_angle

    @min_angle.setter
    def min_angle(self, value):
        if value >= 0 and value <= 180:
            self.__min_angle = value
        else:
            print("Angle Value is invalue - should be between 0 and 180", value)

class PicoCat():
    name = "PicoCat"
    feet = []
    left_foot = Servo(name='FRONT_LEFT')
    feet.append(left_foot)

    def __init__(self):
        print("***", self.name, "is Online ***")

cat = PicoCat()
cat.left_foot.angle = 5
sleep(1)
cat.left_foot.angle = 90
sleep(1)
cat.left_foot.angle = 180
sleep(1)

cat.left_foot.show()