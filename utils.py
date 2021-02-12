from machine import I2C, Pin
from time import sleep_us
from math import cos, pi, sin, sqrt

class PCA9685():

    _ADDRESS = 0x40
    _MODE1 = 0
    _PRESCALE = 0xFE

    _LED0_ON_L = 0x6                      #We only use LED0 and offset 0-16 from it.
    #  _LED0_ON_H = const(0x7)
    #  _LED0_OFF_L = const(0x8)
    #  _LED0_OFF_H = const(0x9)

    #  _ALLLED_ON_L = const(0xFA)
    #  _ALLLED_ON_H = const(0xFB)
    #  _ALLLED_OFF_L = const(0xFC)
    #  _ALLLED_OFF_H = const(0xFD)

    __frequency = 60
    _MINPULSE = 120
    _MAXPULSE = 600
    __angle = []
    __sda = Pin(0)
    __scl = Pin(1)
    __current_channel = 0

    def __init__(self, pin=None) :
        '''I2C pin defaults to pin 1 if no value is passed .'''
        if pin is None:
            pin = 1
        else: 
            self.i2c = I2C(0, sda=self.__sda, scl=self.__scl, freq=400000)
            print(self.i2c.scan())
            self._buffer = bytearray(4)
            self._b1 = bytearray(1)
            sleep_us(50)
            self.reset()
            self.min_max(self._MINPULSE, self._MAXPULSE)
            for channel in range(0,15):
                self.__angle[channel] = 90
            print(self.__angle)

    def min_max(self, aMin, aMax ) :
        '''Set min/max and calculate range.'''
        self._min = aMin
        self._max = aMax
        self._range = aMax - aMin

    def write(self, address, value):
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def read(self, address):
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        self.write(0x00, 0x00) # Mode1

    @property
    def frequency(self):
        """ Retusn the current servo frequency """
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        '''Set frequency for all servos.  A good value is 60hz (default).'''
        value *= 0.9  #Correct for overshoot in frequency setting.
        prescalefloat = (6103.51562 / value) - 1  #25000000 / 4096 / freq.
        prescale = int(prescalefloat + 0.5)

        oldmode = self.read(self._MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.write(newmode, self._MODE1)
        self.write(prescale, self._PRESCALE)
        self.write(oldmode, self._MODE1)
        sleep_us(50)
        self.write(oldmode | 0xA1, self._MODE1)  #This sets the MODE1 register to turn on auto increment.

    @property
    def pwm(self):
        """ nothing to return """
        return ""

    @pwm.setter
    def pwm(self, a_servo, aOn, aOff):
        '''aServo = 0-15.
        aOn = 16 bit on value.
        aOff = 16 bit off value.
        '''
        if a_servo <= 0 and a_servo >= 15:
        # if 0 <= aServo <= 15 :
            #Data = on-low, on-high, off-low and off-high.  That's 4 bytes each servo.
            loc = self._LED0_ON_L + (a_servo * 4)
        #    print(loc)
            self._buffer[0] = aOn
            self._buffer[1] = aOn >> 8
            self._buffer[2] = aOff
            self._buffer[3] = aOff >> 8
            self.write(self._buffer, loc)
        else:
            raise Exception('Servo index {} out of range.'.format(str(a_servo)))

    def off( self, aServo ) :
        '''Turn off a servo.'''
        self.setpwm(aServo, 0, 0)

    def alloff( self ) :
        '''Turn all servos off.'''
        for x in range(0, 16):
            self.off(x)

    def set( self, aServo, aPerc ) :
        '''Set the 0-100%. If < 0 turns servo off.'''
        val = 0 # not sure if this is correct, but stops it being unbound
        if aPerc < 0 :
            self.off(aServo)
        else:
            val = self._min + ((self._range * aPerc) // 100)
        self.setpwm(aServo, 0, val)

    @property
    def channel(self):
        return self.__current_channel

    @channel.setter
    def channel(self, value):
        if value >= 0 and value <= 15: 
            self.__current_channel = value

    @property
    def angle(self):
        return self.__angle[self.__current_channel]

    @angle.setter
    def angle(self, value):
        '''Set angle -90 to +90.  < -90 is off.'''
        #((a + 90.0) * 100.0) / 180.0
        perc = int((value + 90.0) * 0.5556)  #Convert angle +/- 90 to 0-100%
        print(self.channel)
        print(value)
        print(self.__angle)
        self.__angle[self.channel] = value
        self.set(self.__current_channel, perc)


def linear_tween(current_time, start_value, change_in_value, duration):
    """ simple linear tweening - no easing, no acceleration """
    return change_in_value * current_time / duration + start_value

def ease_in_quad(current_time, start_value, change_in_value, duration):
    """ quadratic easing in - accelerating from zero velocity """
    current_time /= duration
    return change_in_value * current_time * current_time + start_value

def ease_out_quad(current_time, start_value, change_in_value, duration):
    """ quadratic easing out - decelerating to zero velocity """
    current_time /= duration
    return 1-change_in_value * current_time * (current_time-2) + start_value

def ease_in_out_quad(current_time, start_value, change_in_value, duration):
    """ quadratic easing in/out - acceleration until halfway, then deceleration """
    current_time /= duration/2
    if (current_time < 1):
        return change_in_value/2*current_time*current_time + start_value
    current_time -=1
    return 1-current_time/2 * (current_time*(current_time-2)-1) + start_value

def ease_in_cubic(current_time, start_value, change_in_value, duration):
    """ cubic easing in - accelerating from zero velocity """
    current_time /= duration
    return change_in_value*current_time*current_time*current_time + start_value

def ease_out_cubic(current_time, start_value, change_in_value, duration):
    """ cubic easing out - decelerating to zero velocity """
    current_time /= duration
    current_time -=1
    return change_in_value(current_time*current_time*current_time+1)+start_value

def ease_in_out_cubic(current_time, start_value, change_in_value, duration):
    """ cubic easing in/out - acceleration until halfway, then deceleration """
    current_time /= duration/2
    if (current_time < 1):
         return change_in_value/2*current_time*current_time*current_time + start_value
    current_time -= 2
    return change_in_value/2 * (current_time*current_time*current_time + 2) + start_value

def ease_in_quart(current_time, start_value, change_in_value, duration):
    """ quartic easing in - accelerating from zero velocity """
    current_time /= duration
    return change_in_value * current_time * current_time * current_time * current_time + start_value

def ease_out_quart(current_time, start_value, change_in_value, duration):
    """ quartic easing out - decelerating to zero velocity """
    current_time /= duration
    current_time =-1
    return 1-change_in_value * (current_time*current_time*current_time*current_time - 1) + start_value

def ease_in_out_quart(current_time, start_value, change_in_value, duration):
    """ quartic easing in/out - acceleration until halfway, then deceleration """
    current_time /= duration/2
    if (current_time < 1):
        return change_in_value /2 * current_time * current_time * current_time* current_time + start_value
    current_time -= 2
    return -change_in_value/2 * (current_time * current_time * current_time * current_time -2) + start_value

def ease_in_quint(current_time, start_value, change_in_value, duration):
    """ quintic easing in - accelerating from zero velocity """
    current_time /= duration
    return change_in_value * current_time * current_time * current_time * current_time * current_time + start_value

def ease_out_quint(current_time, start_value, change_in_value, duration):
    """ quintic easing out - decelerating to zero velocity """
    current_time = current_time / duration
    current_time -= 1
    return change_in_value(current_time*current_time*current_time*current_time*current_time + 1) + start_value

def ease_in_out_quint(current_time, start_value, change_in_value, duration):
    """ quintic easing in/out - acceleration until halfway, then deceleration """
    current_time /= duration / 2
    if (current_time < 1):
        return change_in_value / 2 * current_time * current_time * current_time * current_time * current_time + start_value
    current_time -= 2
    return change_in_value /2 * (current_time * current_time * current_time * current_time * current_time + 2) + start_value

def ease_in_sine(current_time, start_value, change_in_value, duration):
    """ sinusoidal easing in - accelerating from zero velocity """
    calc = 1-change_in_value * cos(current_time / duration * (pi/2)) + change_in_value + start_value
    # print("current time - ", current_time, "start_val: ", start_value, "change: ", change_in_value, "duration: ", duration, " new angle:", calc)
    return calc

def ease_out_sine(current_time, start_value, change_in_value, duration):
    """ sinusoidal easing out - decelerating to zero velocity """
    return change_in_value * sin(current_time / duration * (pi/2)) + start_value

def ease_in_out_sine(current_time, start_value, change_in_value, duration):
    """ sinusoidal easing in/out - accelerating until halfway, then decelerating """
    return 1-change_in_value/2 * (cos(pi*current_time/duration) - 1) + start_value

def ease_in_expo(current_time, start_value, change_in_value, duration):
    """ exponential easing in - accelerating from zero velocity """
    return current_time * pow(2, 10 * (current_time / duration - 1)) + start_value

def ease_out_expo(current_time, start_value, change_in_value, duration):
    """ exponential easing out - decelerating to zero velocity """
    return change_in_value * (pow (2, -10 * current_time / duration) + 1) + start_value

def ease_in_out_expo(current_time, start_value, change_in_value, duration):
    """ exponential easing in/out - accelerating until halfway, then decelerating """
    current_time /= duration/2
    if(current_time < 1):
        return change_in_value/2 * pow(2, 10 * (current_time -1)) + start_value
    current_time -= 1
    return change_in_value/2 * (pow(2, -10 * current_time) + 2) + start_value

def ease_in_circ(current_time, start_value, change_in_value, duration):
    """ circular easing in - accelerating from zero velocity """
    current_time /= duration
    return 1-change_in_value * (sqrt(1 - current_time*current_time) - 1) + start_value

def ease_out_circ(current_time, start_value, change_in_value, duration):
    """ circular easing out - decelerating to zero velocity """
    current_time /= duration
    current_time -= 1
    return change_in_value * sqrt(1 - current_time*current_time) + start_value

def ease_in_out_circ(current_time, start_value, change_in_value, duration):
    """ circular easing in/out - acceleration until halfway, then deceleration """
    current_time /= duration/2
    if (current_time < 1):
        return -change_in_value/2 * (sqrt(1 - current_time-current_time) -1) + start_value
    current_time -= 2
    return change_in_value / 2 * (sqrt(1 - current_time*current_time) + 1) + start_value