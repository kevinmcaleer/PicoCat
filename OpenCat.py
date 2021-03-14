# PicoCat
# 31 January 2020
# Kevin McAleer

from machine import Pin, I2C
from time import sleep, time, ticks_us
from servo import Servo
from pca9685 import PCA9685

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

class Leg():
    
    __name = "leg"
    stand = False

    def __init__(self, i2c, pca9685, shoulder_pin, foot_pin, name=None):
        self.shoulder = Servo(i2c=i2c, pca9685=pca9685, name='shoulder', channel=shoulder_pin)
        self.foot = Servo(i2c=i2c, pca9685=pca9685, name="foot", channel=foot_pin)
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
        # self.shoulder.duration_in_seconds = 0.5 
        self.shoulder.duration_in_seconds = 2
        # self.foot.duration_in_seconds = 0.5
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

    def sit(self):
        print("sitting down leg", self.name)
        self.shoulder.transition = 'ease_in_sine'
        self.foot.transition = 'ease_in_sine'
        self.shoulder.duration_in_seconds = 2 
        self.foot.duration_in_seconds = 2
        self.shoulder.target_angle = 0
        self.foot.target_angle = 180
        self.shoulder.start_angle = 90
        self.shoulder.change_in_value = self.shoulder.target_angle - self.shoulder.start_angle
        self.foot.start_angle = 90
        self.foot.change_in_value = self.foot.target_angle - self.shoulder.start_angle

        # Start the counters
        self.shoulder.tick_start()
        self.foot.tick_start()

    @property
    def stand_tick(self):
        if not self.shoulder.tick() or self.foot.tick():
            self.shoulder.tick()
            self.foot.tick()
        
            # show current values
            self.foot.show()
            self.shoulder.show()
            return False
        else:
            return True 

    @stand_tick.setter
    def stand_tick(self):
        if self.shoulder.elapsed_time_in_seconds <= self.shoulder.duration_in_seconds:
            self.stand_tick = False
        else:
            self.stand_tick = True

class PicoCat():
    name = "PicoCat"
    legs = []
    sda = Pin(0)
    scl = Pin(1)
    id = 0

    def __init__(self):
        self.i2c = I2C(id=self.id, sda=self.sda, scl=self.scl) 
        self.pca9685 = PCA9685(self.i2c)
        back_left = Leg(self.i2c, pca9685=self.pca9685, name="BACK_LEFT", shoulder_pin=Limbs.BACK_LEFT_LEG, foot_pin=Limbs.BACK_LEFT_FOOT)
        back_right = Leg(self.i2c, pca9685=self.pca9685, name="BACK_RIGHT", shoulder_pin=Limbs.BACK_RIGHT_LEG, foot_pin=Limbs.BACK_RIGHT_FOOT)
        front_left = Leg(self.i2c, pca9685=self.pca9685, name='FRONT_LEFT', shoulder_pin=Limbs.FRONT_LEFT_LEG, foot_pin=Limbs.FRONT_LEFT_FOOT)
        front_right = Leg(self.i2c, pca9685=self.pca9685, name='FRONT_RIGHT', shoulder_pin=Limbs.FRONT_RIGHT_LEG, foot_pin=Limbs.FRONT_RIGHT_FOOT)

        self.legs.append(front_left)
        self.legs.append(front_right)
        self.legs.append(back_left)
        self.legs.append(back_right)

        print("***", self.name, "is Online ***")

    def stand(self):   
        print("Stand!")
        for limb in self.legs:
            limb.stand()

        
    def sit(self):
        print("Sit!")
        for limb in self.legs:
            limb.sit()
    

cat = PicoCat()
cat.stand()

for limb in cat.legs:
    print("limb status:", limb.stand_tick)
    while not limb.stand_tick:
        print("not stand_tick")
        limb.stand_tick

sleep(1)
cat.sit()

for limb in cat.legs:
    
    while not limb.stand_tick:
        print("not stand_tick")
        limb.stand_tick