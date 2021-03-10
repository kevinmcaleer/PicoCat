from pca import PCA9685
# from picocat import Servos
from machine import I2C, Pin
from servo import Servos

sda = Pin(0)
scl = Pin(1)
id = 0
i2c = I2C(id=id, sda=sda, scl=scl)

pca = PCA9685(i2c=i2c)
# pca.i2c = i2c
servo = Servos(i2c=i2c)
servo.position(index=0, degrees=180)