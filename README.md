# PicoCat
>OpenCat - MicroPython core by Kevin McAleer
For the Raspberry Pi Pico

---

This project has the following goals:
- create a Python based code to control the cat
- Implement inverse kinematics
- Implement smoother Motion transitions, include Ease-in, Ease-Out, Easy-Ease
- Self Balancing code to keep the robot upright
- Create code to self right the robot if it goes upside down
- upgrade the servos from SG90s to MG90s

- Approach - how we will approach this project
- Modelling Servos
- Reading Telemetry data
- Bluetooth Control
- Inverse kinematics
- Transitions and smooth animation of servo movements - ease in, ease out, linear, time based not delay based.

# Classes:
1. Servo
    - angle
    - name
    - pin
    - max_angle
    - min_angle
1. PicoCat
    - stand
    - sit
    - wag
    - name
1. MPU6050
1. RangeFinder