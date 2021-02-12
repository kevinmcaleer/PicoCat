from machine import Pin, I2C
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
    __angle = {0 : 90, 1: 90, 2:90, 3:90, 4:90,5:90,6:90,7:90,8:90,9:90,10:90,11:90,12:90,13:90,14:90,15:90}
    __sda = Pin(0)
    __scl = Pin(1)
    __current_channel = 0
    _min = 0
    _max = 180
    _range = 180

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

    def min_max(self, min, max ) :
        '''Set min/max and calculate range.'''
        self._min = min
        self._max = max
        self._range = max - min

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
        self.pwm(aServo, 0, val)

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
