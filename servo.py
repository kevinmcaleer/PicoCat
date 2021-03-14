# servo.py
# Kevin McAleer
# March 2021
# PicoCat


from transition import Transition
from time import sleep, ticks_us

def map_angle(x, in_min, in_max, out_min, out_max):
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

    def _us2duty(self, value):
        return int(4095 * value / self.period)

    def __init__(self, i2c, pca9685, name=None, pin=None, channel=None, address=0x40, 
                 freq=50, min_us=600, max_us=2400, degrees=180):

        self.period = 1000000 / freq
        self.min_duty = self._us2duty(min_us)
        self.max_duty = self._us2duty(max_us)
        self.degrees = degrees
        self.freq = freq
        self.pca9685 = pca9685
        self.pca9685.freq(freq)
        if channel is None:
            self.__channel = 0
        else:
            self.__channel = channel
            print("Channel set to", channel)
        if name is not None:
            print(name)
            self.__name = name
            
        if pin is not None:
            print(pin)
            self.__pin = pin
        
    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, channel_value):
        if channel_value <= 15 and channel_value >= 0:
            self.__channel = channel_value
        else:
            print("Error - the channel value was out of range, expected between 0 and 15, got,", channel_value)

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
        print("Name: ", self.name, "Pin:", self.pin, "Current Angle:", self.current_angle)
        # print("Pin: ", self.pin)
        # print("Current Angle:", self.current_angle) 

  
    def angle(self, angle_value, channel):
        ''' Sets the angle, in degrees '''
        # print("setting angle for channel", self.channel, "to angle", angle_value)
        if ((angle_value >= 0) and (angle_value > self.min_angle)) and ((angle_value <= 180) and (angle_value <self.max_angle)):
            self.__current_angle = angle_value

            # map values - degrees to duty
            
            duty = map_angle(angle_value, 0, 180, 0, 4096)
            # print("Duty is:", duty, "angle requested is", angle_value)
            # self.__pwm.duty_u16(my_angle)
            self.pca9685.duty(index=channel, value=duty)
            
            sleep(0.0001)
        else:
            print("Angle value less than 0 or greater than 180", angle_value)

    def release(self, channel):
        ''' release the break '''
        self.pca9685.duty(channel, 0)

    @property
    def current_angle(self):
        return self.__current_angle

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
        """ In microseconds """
        return self.__duration
    
    @duration.setter
    def duration(self, value_in_microseconds):
        """ In microseconds """
        self.__duration = value_in_microseconds

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
        """ In microseconds """
        return self.__current_time - self.__tick_start_time

    @property
    def elapsed_time_in_seconds(self):
        """ In seconds """
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
            # print("target angle for", self.name, "set to: ", self.__target_angle)
        else:
            print("Target Angle out of range - Min:", self.__min_angle, " Max: ", self.__max_angle, " angle provided: ", value)

    @property
    def change_in_value(self):
        return self.__change_in_value

    @change_in_value.setter
    def change_in_value(self, value):
        self.__change_in_value = value

    def show(self):
        print("name: ", self.name, 
              "Angle", self.current_angle, 
              "start time", self.__tick_start_time, 
              "elapsed time: ", self.elapsed_time_in_seconds,
              "target angle:", self.target_angle,
              "Transition type:", self.transition,
              "current angle:", self.__current_angle)

    def tick_start(self):
        self.__tick_start_time = ticks_us()

    def tick(self):
        # print("tick: ", self.name)
        self.__current_time = ticks_us()
        elapsed_time = self.elapsed_time
        if elapsed_time >= self.duration:
            return True
        cur_angle = self.__current_angle
        valid_transition = False
        # print("transition type is: ", self.__transition)
        if self.__transition == 'linear_tween':
            cur_angle = Transition().linear_tween(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_circ':
            cur_angle = Transition().ease_in_circ(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_cubic':
            cur_angle = Transition().ease_in_cubic(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quad':
            cur_angle = Transition().ease_in_quad(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quart':
            cur_angle = Transition().ease_in_quart(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_expo':
            cur_angle = Transition().ease_in_expo(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quart':
            cur_angle = Transition().ease_in_quart(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if self.__transition == 'ease_in_quint':
            cur_angle = Transition().ease_in_quint(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)       
            valid_transition = True         
        if self.__transition == 'ease_in_sine':
            cur_angle = Transition().ease_in_sine(current_time=self.elapsed_time,
                         start_value=self.start_angle,
                         change_in_value=self.change_in_value,
                         duration=self.duration)
            valid_transition = True
        if not valid_transition:
            print("error - No Valid Transition provided")
        # print(self.name, int(cur_angle))
        cur_angle = int(cur_angle)
        self.angle(angle_value=cur_angle, channel=self.channel)
        
        if self.current_angle == self.target_angle:
            return True
        else:
            return False