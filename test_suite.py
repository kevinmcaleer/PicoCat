import unittest
from transition import Transition
from time import time

# This is a comment

def map_angle(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

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


def tick(start_time, start_angle, change_in_value, duration, target_angle):
    current_time = current_milli_time()
    elapsed_time = start_time - current_time
    cur_angle = Transition().ease_in_out_sine(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, target_angle=target_angle)   
    return cur_angle

class Test_suite(unittest.TestCase):

    def test_linear_tween(self):
        print("testing linear tween")
        dur = Duration()
        dur.duration_in_seconds = .0001
        duration = int(dur.duration)
        target_angle = 180
        start_angle = 90
        current_angle = 90
        # duration = 10
        start_time = current_milli_time()
        # print("start time", start_time)
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().linear_tween(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
        self.assertEqual(cur_angle,target_angle)

    def test_lineartween_down(self):
        print("testing linear tween decreasing values")
        dur = Duration()
        dur.duration_in_seconds = .0001
        duration = int(dur.duration)
        target_angle = 0
        start_angle = 180
        current_angle = 90
        # duration = 10
        start_time = current_milli_time()
        # print("start time", start_time)
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().linear_tween(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
        self.assertEqual(cur_angle,target_angle)

    def test_lineartween_down_small(self):
        print("testing linear tween down small values")
        dur = Duration()
        dur.duration_in_seconds = .001
        duration = int(dur.duration)
        target_angle = 1
        start_angle = 0
        current_angle = 90
        # duration = 10
        start_time = current_milli_time()
        # print("start time", start_time)
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration, target_angle)
            cur_angle = Transition().linear_tween(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)
        self.assertEqual(cur_angle,target_angle)

    def test_ease_in_quad_up(self):
        print("testing ease in quad increasing values")
        dur = Duration()
        dur.duration_in_seconds = .001
        duration = int(dur.duration)
        target_angle = 180
        start_angle = 0
        current_angle = 90
        # duration = 10
        start_time = current_milli_time()
        # print("start time", start_time)
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().ease_in_quad(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
        self.assertEqual(cur_angle,target_angle)

    def test_ease_in_quad_down(self):
        print("testing ease in quad decreasing values")
        dur = Duration()
        dur.duration_in_seconds = .001
        duration = int(dur.duration)
        target_angle = 90
        start_angle = 180
        current_angle = 90
        # duration = 10
        start_time = current_milli_time()
        # print("start time", start_time)
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().ease_in_quad(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
        self.assertEqual(cur_angle,target_angle)

    def test_ease_out_quad_down(self):
        print("testing ease out quad decreasing values")
        dur = Duration()
        dur.duration_in_seconds = .001
        duration = int(dur.duration)
        target_angle = 90
        start_angle = 180
        current_angle = 90
        # duration = 10
        start_time = current_milli_time()
        # print("start time", start_time)
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().ease_out_quad(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
        self.assertEqual(cur_angle,target_angle)

    def test_ease_out_quad_up(self):
        print("testing ease out quad increasing values")
        dur = Duration()
        dur.duration_in_seconds = .0001
        duration = int(dur.duration)
        target_angle = 180
        start_angle = 0
        current_angle = 90
        start_time = current_milli_time()
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().ease_out_quad(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
            # print("time:", current_time, "angle", cur_angle, "target_angle",target_angle, "elapsed time", elapsed_time, "duration", duration)
        self.assertEqual(cur_angle,target_angle)

    def test_ease_in_out_quad_up(self):
        print("testing ease in-out quad increasing values")
        dur = Duration()
        dur.duration_in_seconds = .0001
        duration = int(dur.duration)
        target_angle = 180
        start_angle = 0
        current_angle = 90
        start_time = current_milli_time()
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().ease_in_out_quad(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
            # print("time:", current_time, "angle", cur_angle, "target_angle",target_angle, "elapsed time", elapsed_time, "duration", duration)
        self.assertEqual(cur_angle,target_angle)

    def test_ease_in_out_quad_down(self):
        print("testing ease in-out quad decreasing values")
        dur = Duration()
        dur.duration_in_seconds = .0001
        duration = int(dur.duration)
        target_angle = 0
        start_angle = 180
        current_angle = 90
        start_time = current_milli_time()
        change_in_value = target_angle - start_angle

        # loop
        current_time = current_milli_time()
        elapsed_time = current_time - start_time

        while int(elapsed_time) <= int(duration) or (cur_angle == target_angle-1):
            current_time = current_milli_time()
            elapsed_time = current_time - start_time 
            # angle = tick(start_time, start_angle, change_in_value, duration)
            cur_angle = Transition().ease_in_out_quad(current_time=elapsed_time,
                            start_value=start_angle,
                            change_in_value=change_in_value,
                            duration=duration, 
                            start_time=start_time, 
                            target_angle=target_angle)   
            # print("time:", current_time, "angle", cur_angle, "target_angle",target_angle, "elapsed time", elapsed_time, "duration", duration)
        self.assertEqual(cur_angle,target_angle)

    def test_map_angle_100(self):
        print("testing map angle equal")
        angle = map_angle(x=10, in_min=0, in_max=100, out_min=0, out_max=100)
        self.assertEqual(angle, 10)
    
    def test_map_angle_10(self):
        print("testing map angle 10 percent maller")
        angle = map_angle(x=10, in_min=0, in_max=100, out_min=0, out_max=10)
        self.assertEqual(angle, 1)

if __name__ == '__main__':
    unittest.main()