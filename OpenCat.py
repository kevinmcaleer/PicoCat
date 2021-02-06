# PicoCat
# 31 January 2020
# Kevin McAlee

from machine import Pin, PWM
from time import sleep, time, ticks_us
from utils import ease_in_circ, ease_in_cubic, ease_in_expo, ease_in_out_circ, ease_in_out_cubic, ease_in_out_expo, ease_in_out_quad, ease_in_out_quart, ease_in_out_quint, ease_in_out_sine, ease_in_quad, ease_in_quart, ease_in_sine, ease_out_circ, ease_out_cubic, ease_out_expo, ease_out_quad, ease_out_quart, ease_out_quint, ease_out_sine, linear_tween, ease_in_quint
from utils import PCA9685

class Limbs():
    """
    setup legs and feet to correspond to the correct channel
    """
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

class Transition():
    linear_tween = 0
    ease_in_circ = 0
    ease_in_cubic = 1
    ease_in_expo = 2
    ease_in_quad = 3
    ease_in_quart = 4
    ease_in_quint = 5
    ease_in_sine = 6

    ease_in_out_circ = 7
    ease_in_out_cubic = 8
    ease_in_out_expo = 9
    ease_in_out_quad = 10
    ease_in_out_quart = 11
    ease_in_out_quint = 12
    ease_in_out_sine = 13

    ease_out_circ = 14
    ease_out_cubic = 15
    ease_out_expo = 16
    ease_out_quad = 17
    ease_out_quart = 18
    ease_out_quint = 19 
    ease_out_sine = 20
    


def map(x, in_min, in_max, out_min, out_max):
    # if x == 0:
    #     x = 1
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)


class Servo():
    """ Models a cats foot """
    __name = ""                   # The name of the Foot - Front_Right etc
    __current_angle = 90        # the current angle of the servo
    __transition = "ease_in_sine"  # the transition type for easing in and out
    __duration = 0.5            # the duration of the transition in ms (ie 1000000 = 1 second)
    __channel = 0               # the channel of the PWM servo (for PCA9685)
    __pin = 0                   # the pin that the servo is connected to (if not using PCA9685)
    __max_angle = 180
    __min_angle = 0
    __target_angle = 0          # Used for Easing
    __current_time = 0          # Used for Easing
    __start_value = 0           # Used for Easing
    __change_in_value = 0       # Used for Easing
    __target_angle = 90         # Used for Easing
    __tick_started = False      # Used for Easing
    __tick_start_time = 0       # Used for Easing

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

    @property
    def target_angle(self):
        return self.__target_angle
    
    @target_angle.setter
    def target_angle(self, value):
        self.__target_angle = value

    @property
    def transition(self):
        return self.__transition
    
    @transition.setter
    def transition(self, value):
        if value in ['linear_tween','ease_in_circ','ease_in_cubic','ease_in_expo','ease_in_quad','ease_in_quart','ease_in_quint','ease_in_sine',
                     'ease_in_out_circ', 'ease_in_out_cubic', 'ease_in_out_expo', 'ease_in_out_quad', 'ease_in_out_quart', 'ease_in_out_quint', 'ease_in_out_sine',
                     'ease_out_circ', 'ease_out_cubic', 'ease_out_expo', 'ease_out_quad', 'ease_out_quart', 'ease_out_quint', 'ease_out_sine']:
            self.__transition = value
        else:
            print("Value is not a valid transition type")

    @property
    def duration(self):
        return self.__duration
    
    @duration.setter
    def duration(self, value):
        self.__duration = value

    @property 
    def duration_in_seconds(self):
        """ Returns the duration in seconds """
        return self.__duration / 1000000

    @duration_in_seconds.setter
    def duration_in_seconds(self, value):
        """ Sets the duration in seconds """
        self.__duration = (value * 1000000)

    @property
    def elapsed_time(self):
        return self.__current_time - self.__tick_start_time

    @property
    def elapsed_time_in_seconds(self):
        return self.elapsed_time / 1000000


    @property
    def target_angle(self):
        return self.__target_angle

    @property
    def start_angle(self):
        return self.__start_value
    
    @start_angle.setter
    def start_angle(self, value):
        if value <= self.__max_angle and value >= self.__min_angle:
            self.__start_value = value
        else:
            print("error - angle provided is outside the valid range - Max Angle: ", self.__max_angle, " Min Angle: ", self.__min_angle, " Angle provided: ", value)

    @target_angle.setter
    def target_angle(self, value):
        if value <= self.__max_angle and value >= self.__min_angle:
            self.__target_angle = value
            print("target angle set to:, ", self.__target_angle)
        else:
            print("Target Angle out of range - Min:", self.__min_angle, " Max: ", self.__max_angle, " angle provided: ", value)

    @property
    def change_in_value(self):
        return self.__change_in_value

    @change_in_value.setter
    def change_in_value(self, value):
        self.__change_in_value = value

    def show(self):
        print("name: ", self.name)
        print("angle: ", self.angle)
        print("start time", self.__tick_start_time)
        print("elapsed time: ", self.elapsed_time_in_seconds)
        print("target angle:", self.target_angle)
        print("Transition type:", self.transition)
        print("current angle:", self.__current_angle)

    def tick_start(self):
        self.__tick_start_time = ticks_us()

    def tick(self):
        self.__current_time = ticks_us()
        elapsed_time = self.elapsed_time
        if elapsed_time >= self.duration:
            return True
        # print("Duration in MS is: ", self.duration)
        # print("Start time is: ", self.__tick_start_time)
        # print("Current time:", self.__current_time)
        # print("Elapsed time = ", (self.elapsed_time_in_seconds))
        cur_angle = self.__current_angle
        valid_transition = False
        # print("transition type is: ", self.__transition)
        if self.__transition == 'linear_tween':
            cur_angle = linear_tween(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_circ':
            cur_angle = ease_in_circ(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_cubic':
            cur_angle = ease_in_cubic(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quad':
            cur_angle = ease_in_quad(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quart':
            cur_angle = ease_in_quart(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_expo':
            cur_angle = ease_in_expo(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quart':
            cur_angle = ease_in_quart(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quint':
            cur_angle = ease_in_quint(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)       
            valid_transition = True         
        if self.__transition == 'ease_in_sine':
            cur_angle = ease_in_sine(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True

        if not valid_transition:
            print("error - No Valid Transition provided")
        # print(self.name, int(cur_angle))
        self.angle = int(cur_angle)
        
        if self.angle == self.target_angle:
            return True
        else:
            return False

class Leg():
    
    __name = "leg"

    def __init__(self, shoulder_pin, foot_pin, name=None):
        self.shoulder = Servo(name='shoulder', pin=shoulder_pin)
        self.foot = Servo(name="foot", pin=foot_pin)
        if name is not None:
            self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def stand(self):
        print("standing up leg", self.name)
        self.shoulder.transition = 'ease_in_sine'
        self.foot.transition = 'ease_in_sine'
        self.shoulder.duration_in_seconds = 2 
        self.foot.duration_in_seconds = 2
        self.shoulder.target_angle = 180
        self.foot.target_angle = 180
        self.shoulder.start_angle = 90
        self.shoulder.change_in_value = self.shoulder.target_angle - self.shoulder.start_angle
        self.foot.start_angle = 90
        self.foot.change_in_value = self.foot.target_angle - self.shoulder.start_angle

        # Start the counters
        self.shoulder.tick_start()
        self.foot.tick_start()

        while self.shoulder.elapsed_time_in_seconds <= self.shoulder.duration_in_seconds:
            # print("ticking...")
            print(self.shoulder.name, self.shoulder.elapsed_time_in_seconds, self.shoulder.angle)
            self.shoulder.tick()
            self.foot.tick()

        # show current values
        self.foot.show()
        self.shoulder.show()

class PicoCat():
    name = "PicoCat"
    legs = []
    __pca9685 = PCA9685()

    def __init__(self):
        back_left = Leg(name="BACK_LEFT", shoulder_pin=Limbs.BACK_LEFT_LEG, foot_pin=Limbs.BACK_LEFT_FOOT)
        back_right = Leg(name="BACK_RIGHT", shoulder_pin=Limbs.BACK_RIGHT_LEG, foot_pin=Limbs.BACK_RIGHT_FOOT)
        front_left = Leg(name='FRONT_LEFT', shoulder_pin=Limbs.FRONT_LEFT_LEG, foot_pin=Limbs.FRONT_LEFT_FOOT)
        front_right = Leg(name='FRONT_RIGHT', shoulder_pin=Limbs.FRONT_RIGHT_LEG, foot_pin=Limbs.FRONT_RIGHT_FOOT)

        self.legs.append(front_left)
        self.legs.append(front_right)
        self.legs.append(back_left)
        self.legs.append(back_right)

        print("***", self.name, "is Online ***")

    def stand(self):   
        for servo in self.legs:
            servo.stand()
    

cat = PicoCat()
cat.stand()