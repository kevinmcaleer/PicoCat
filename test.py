from pca9685 import PCA9685
# from picocat import Servos
from machine import I2C

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = I2C(0, sda=sda, scl=scl)
# s = Servos(i2c)
# s.position(0, degrees=90)


pca = PCA9685()
# pca.i2c = i2c
pca.channel = 1
pca.angle = 90
