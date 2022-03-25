# January 2021
# Kevin McAleer
# PicoCat.py

from time import sleep, ticks_us
from machine import PWM, Pin
# from utils import PCA9865
from transition import Transition

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)

class Limbs():
    """ Setup Legs and feet to correspond to the correct channels """
    FRONT_LEFT_LEG = 0
    FRONT_RIGHT_LEG = 1
    BACK_LEFT_LEG = 2
    BACK_RIGHT_LEG = 3
    FRONT_LEFT_FOOT = 4
    FRONT_RIGHT_FOOT = 5
    BACK_LEFT_FOOT = 6
    BACK_RIGHT_FOOT = 7
    TAIL = 8
    NECK = 9
    HEAD = 10


class Servo():
    __angle = 90
    __name = "Servo"
    __pin = 0
    __max_angle = 180
    __min_angle = 0
    __current_angle = 90
    __transition = "ease_in_sine"
    __duration = 0.5 # this is in seconds
    __channel = 0
    __pin = 0
    __target_angle = 0
    __current_time = 0
    __start_value = 0
    __change_in_value = 0
    __tick_started = False
    __tick_start_time = 0
    elapsed_time = 0

    def tick_start(self):
        self.__tick_start_time = ticks_us()

    def tick(self):
        self.__current_time = ticks_us()
        elapsed_time = self.elapsed_time
        if elapsed_time >= self.__duration:
            return True
        
        cur_angle = self.__current_angle

        if self.__transition == 'ease_in_sine':
            cur_angle = Transition().ease_in_sine(current_time=self.elapsed_time, 
                                                  start_value=self.__start_value, 
                                                  change_in_value=self.__start_value-self.__target_angle,
                                                  duration=self.__duration, 
                                                  start_time=ticks_us, target_angle=self.__target_angle)
            self.angle = int(cur_angle)

    def __init__(self, name=None, pin=None):
        if name is not None:
            self.__name = name
        if pin is not None:
            self.__pin = pin
        
        self.__pwm = PWM(Pin(self.__pin))
        self.__pwm.freq(1000)

        print("*** ", self.__name , "is Online ***")

    @property
    def duration_in_seconds(self):
        """ Returns the duration in Microseconds"""
        return self.__duration * 1000000

    @duration_in_seconds.setter
    def duration_in_seconds(self, value):
        self.__duration = value * 1000000

    @property
    def elapsed_time_in_seconds(self):
        """ Returns the elapsed time in seconds"""
        return self.__current_time - self.__tick_start_time / 1000000

    @property 
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        if value <= 180 and value >= 0:
            self.__angle = value

            # Servo Setting Code
            my_angle = map(value, 0, 180, 0, 65025)
            self.__pwm.duty_u16(my_angle)
            sleep(0.01)
            # print("the angle is now", self.angle)
        else:
            print("The angle was too small or too large: ", value) 
    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value 
        print("Hello from", self.__name)
    
    @property 
    def pin(self):
        return self.__pin

    @pin.setter
    def pin(self, value):
        if value >= 0 and value <= 40:
            self.__pin = value 
        else:
            print("The Pin was too low or too large: ", value) 

class Leg():
    __name = "leg"
    
    @property
    def name(self):
        return self.__name 
    
    @name.setter
    def name(self, value):
        self.__name = value 


    def __init__(self, shoulder_pin, foot_pin, name=None):
        self.shoulder = Servo(name='Shoulder', pin=shoulder_pin)
        self.foot = Servo(name="foot", pin=foot_pin)
        if name is not None:
            self.__name = name 

    def stand(self):
        led = Pin(25, Pin.OUT)
        print("Standing Up leg", self.name)
        self.shoulder.__transition = "ease_in_sine"
        self.foot.__transition = "ease_in_sine"

        self.shoulder.duration_in_seconds = 2
        self.shoulder.__target_angle = 180
        self.shoulder.__start_value = 90
        self.shoulder.__change_in_value = self.shoulder.__target_angle - self.shoulder.__start_value

        self.shoulder.tick_start()
        self.foot.tick_start()
        
        while self.shoulder.elapsed_time_in_seconds <= self.shoulder.duration_in_seconds:
            self.shoulder.tick()
            self.foot.tick()


class PicoCat():
    name = "PicoCat"
    legs = []
    # __pca9685 = PCA9865

    def __init__(self):
        back_left = Leg(name="BACK_LEFT", shoulder_pin=Limbs.BACK_LEFT_LEG, foot_pin=Limbs.BACK_LEFT_FOOT)
        back_right = Leg(name="BACK_RIGHT", shoulder_pin=Limbs.BACK_RIGHT_LEG, foot_pin=Limbs.BACK_RIGHT_FOOT)
        front_left = Leg(name="FRONT_LEFT", shoulder_pin=Limbs.FRONT_LEFT_LEG, foot_pin=Limbs.FRONT_LEFT_FOOT)
        front_right = Leg(name="FRONT_RIGHT", shoulder_pin=Limbs.FRONT_RIGHT_LEG, foot_pin=Limbs.FRONT_RIGHT_FOOT)

        self.legs.append(front_left)
        self.legs.append(front_right)
        self.legs.append(back_left)
        self.legs.append(back_right)

        print("*** ", self.name , "is Online ***")

    def stand(self):
        for servo in self.legs:
            servo.stand()

# s = Servo()

# s.name = "Neck"
# s.angle = 10
# sleep(0.5)
# s.angle = 180
# sleep(0.5)
# s.angle = 90
# sleep(0.5)

cat = PicoCat()
cat.stand()
sleep(1)
