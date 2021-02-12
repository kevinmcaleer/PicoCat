from math import sin, cos, pi, sqrt

class Transition():
    
    def ease_in_sine(self, current_time, start_value, change_in_value, duration):
        calc = 1 - change_in_value * cos(current_time / duration * (pi/2)) + change_in_value + start_value
        return calc
