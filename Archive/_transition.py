from math import sin, cos, pi, sqrt

class Transition():
    def linear_tween(self, current_time, start_value, change_in_value, duration):
        """ simple linear tweening - no easing, no acceleration """
        return change_in_value * current_time / duration + start_value

    def ease_in_quad(self, current_time, start_value, change_in_value, duration):
        """ quadratic easing in - accelerating from zero velocity """
        current_time /= duration
        return change_in_value * current_time * current_time + start_value

    def ease_out_quad(self, current_time, start_value, change_in_value, duration):
        """ quadratic easing out - decelerating to zero velocity """
        current_time /= duration
        return 1-change_in_value * current_time * (current_time-2) + start_value

    def ease_in_out_quad(self, current_time, start_value, change_in_value, duration):
        """ quadratic easing in/out - acceleration until halfway, then deceleration """
        current_time /= duration/2
        if (current_time < 1):
            return change_in_value/2*current_time*current_time + start_value
        current_time -=1
        return 1-current_time/2 * (current_time*(current_time-2)-1) + start_value

    def ease_in_cubic(self, current_time, start_value, change_in_value, duration):
        """ cubic easing in - accelerating from zero velocity """
        current_time /= duration
        return change_in_value*current_time*current_time*current_time + start_value

    def ease_out_cubic(self, current_time, start_value, change_in_value, duration):
        """ cubic easing out - decelerating to zero velocity """
        current_time /= duration
        current_time -=1
        return change_in_value(current_time*current_time*current_time+1)+start_value

    def ease_in_out_cubic(self, current_time, start_value, change_in_value, duration):
        """ cubic easing in/out - acceleration until halfway, then deceleration """
        current_time /= duration/2
        if (current_time < 1):
            return change_in_value/2*current_time*current_time*current_time + start_value
        current_time -= 2
        return change_in_value/2 * (current_time*current_time*current_time + 2) + start_value

    def ease_in_quart(self, current_time, start_value, change_in_value, duration):
        """ quartic easing in - accelerating from zero velocity """
        current_time /= duration
        return change_in_value * current_time * current_time * current_time * current_time + start_value

    def ease_out_quart(self, current_time, start_value, change_in_value, duration):
        """ quartic easing out - decelerating to zero velocity """
        current_time /= duration
        current_time =-1
        return 1-change_in_value * (current_time*current_time*current_time*current_time - 1) + start_value

    def ease_in_out_quart(self, current_time, start_value, change_in_value, duration):
        """ quartic easing in/out - acceleration until halfway, then deceleration """
        current_time /= duration/2
        if (current_time < 1):
            return change_in_value /2 * current_time * current_time * current_time* current_time + start_value
        current_time -= 2
        return -change_in_value/2 * (current_time * current_time * current_time * current_time -2) + start_value

    def ease_in_quint(self, current_time, start_value, change_in_value, duration):
        """ quintic easing in - accelerating from zero velocity """
        current_time /= duration
        return change_in_value * current_time * current_time * current_time * current_time * current_time + start_value

    def ease_out_quint(self, current_time, start_value, change_in_value, duration):
        """ quintic easing out - decelerating to zero velocity """
        current_time = current_time / duration
        current_time -= 1
        return change_in_value(current_time*current_time*current_time*current_time*current_time + 1) + start_value

    def ease_in_out_quint(self, current_time, start_value, change_in_value, duration):
        """ quintic easing in/out - acceleration until halfway, then deceleration """
        current_time /= duration / 2
        if (current_time < 1):
            return change_in_value / 2 * current_time * current_time * current_time * current_time * current_time + start_value
        current_time -= 2
        return change_in_value /2 * (current_time * current_time * current_time * current_time * current_time + 2) + start_value

    def ease_in_sine(self, current_time, start_value, change_in_value, duration):
        """ sinusoidal easing in - accelerating from zero velocity """
        calc = 1-change_in_value * cos(current_time / duration * (pi/2)) + change_in_value + start_value
        # print("current time - ", current_time, "start_val: ", start_value, "change: ", change_in_value, "duration: ", duration, " new angle:", calc)
        return calc

    def ease_out_sine(self, current_time, start_value, change_in_value, duration):
        """ sinusoidal easing out - decelerating to zero velocity """
        return change_in_value * sin(current_time / duration * (pi/2)) + start_value

    def ease_in_out_sine(self, current_time, start_value, change_in_value, duration):
        """ sinusoidal easing in/out - accelerating until halfway, then decelerating """
        return 1-change_in_value/2 * (cos(pi*current_time/duration) - 1) + start_value

    def ease_in_expo(self, current_time, start_value, change_in_value, duration):
        """ exponential easing in - accelerating from zero velocity """
        return current_time * pow(2, 10 * (current_time / duration - 1)) + start_value

    def ease_out_expo(self, current_time, start_value, change_in_value, duration):
        """ exponential easing out - decelerating to zero velocity """
        return change_in_value * (pow (2, -10 * current_time / duration) + 1) + start_value

    def ease_in_out_expo(self, current_time, start_value, change_in_value, duration):
        """ exponential easing in/out - accelerating until halfway, then decelerating """
        current_time /= duration/2
        if(current_time < 1):
            return change_in_value/2 * pow(2, 10 * (current_time -1)) + start_value
        current_time -= 1
        return change_in_value/2 * (pow(2, -10 * current_time) + 2) + start_value

    def ease_in_circ(self, current_time, start_value, change_in_value, duration):
        """ circular easing in - accelerating from zero velocity """
        current_time /= duration
        return 1-change_in_value * (sqrt(1 - current_time*current_time) - 1) + start_value

    def ease_out_circ(self, current_time, start_value, change_in_value, duration):
        """ circular easing out - decelerating to zero velocity """
        current_time /= duration
        current_time -= 1
        return change_in_value * sqrt(1 - current_time*current_time) + start_value

    def ease_in_out_circ(self, current_time, start_value, change_in_value, duration):
        """ circular easing in/out - acceleration until halfway, then deceleration """
        current_time /= duration/2
        if (current_time < 1):
            return -change_in_value/2 * (sqrt(1 - current_time-current_time) -1) + start_value
        current_time -= 2
        return change_in_value / 2 * (sqrt(1 - current_time*current_time) + 1) + start_value