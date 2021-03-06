from machine import Pin, I2C

sda = Pin(0)
scl = Pin(1)
id = 0

i2c = I2C(id=id, sda=sda, scl=scl)

print(i2c.scan())
i2c.writeto(64, '\x00')

