from pca9685 import PCA9685
from servo import Servos
from machine import I2C

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = I2C(0, sda=sda, scl=scl)
s = Servos(i2c)
s.position(0, degrees=90)


