from transition import Transition
from time import time_ns, time
# from servo import Servo
t = Transition()

def current_milli_time():
    return round(time() * 1000)

class Duration():
    
    __duration = 0
    
    @property
    def duration_in_seconds(self):
        return self.__duration

    @duration_in_seconds.setter
    def duration_in_seconds(self, value):
        """ Sets the duration in seconds """
        self.__duration = (value * 1000000)
    
    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value


def tick():
    current_time = current_milli_time()
    elapsed_time = start_time - current_time
    cur_angle = Transition().ease_in_out_sine(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration)   
    return cur_angle


dur = Duration()
dur.duration_in_seconds = .01
duration = dur.duration
target_angle = 180
start_angle = 90
current_angle = 90
# duration = 10
start_time = current_milli_time()
print("start time", start_time)
change_in_value = target_angle - start_angle

# loop
current_time = current_milli_time()
elapsed_time = current_time - start_time
while elapsed_time <= duration:
    current_time = current_milli_time()
    elapsed_time = current_time - start_time 

    # current_angle = t.ease_in_sine(current_time=elapsed_time, start_value=start_angle, change_in_value=change_in_value, duration=duration)
    angle = tick()
    print("angle", angle,"current_time", current_time, "duration",duration, "elapsed time", elapsed_time)
