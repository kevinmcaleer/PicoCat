# machine stubb

class Pin():

    OUT = 1

    def __init__(self, value, pin_type):
        print ('created Pin', value, pin_type)

    def on(self):
        print("pin on")
        
    def off(self):
        print("pin off")

class PWM():

    pfreq = 50
    pduty = 77
    def __init__(self, value):
        print('created PWM with value ', value)

    def freq(self, value):
        print('frequency')
        self.pfreq = value 
        return value 

    def duty(self, value):
        print('duty')
        self.pduty = value 
        return value 

class ADC():

    # fake ADC to Digital convertor
    pin = 0

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return 1024

class I2C():
    
    def __init__(id=None, sda=None, scl=None):
        pass
