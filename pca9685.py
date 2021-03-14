# pca9685.py
# Kevin McAleer
# March 2021
'''
@author Kevin McAleer
'''

import ustruct
from time import sleep, sleep_us


class PCA9685:
    """
    This class models the PCA9685 board, used to control up to 16
    servos, using just 2 wires for control over the I2C interface
    """
    def __init__(self, i2c, address=0x40):
        """
        class constructor

        Args:
            i2c ([I2C Class, from the build in machine library]): This is used to 
            bring in the i2c object, which can be created by 
            > i2c = I2C(id=0, sda=Pin(0), scl=Pin(1))
            address (hexadecimal, optional): [description]. Defaults to 0x40.
        """
        self.i2c = i2c
        self.address = address
        self.reset()
        
    def _write(self, address, value):
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address):
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        self._write(0x00, 0x00) # Mode1
        print("reseting I2C")
        sleep(0.1)


    def freq(self, freq=None):
        if freq is None:
            return int(25000000.0 / 4096 / (self._read(0xfe) - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        sleep_us(5)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on

    def pwm(self, index, on=None, off=None):
        if on is None or off is None:
            data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index,  data)

    def duty(self, index, value=None, invert=False):
        if value is None:
            value = int(4096 / 2)
            # pwm = self.pwm(index)
            # if pwm == (0, 4096):
            #     value = 0
            # elif pwm == (4096, 0):
            #     value = 4095
            # value = pwm[1]
            # if invert:
            #     value = 4095 - value
            return value
        
        if not 0 <= value <= 4095:
            raise ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)