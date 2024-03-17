#!/usr/bin/env python3

"""
Starting file to be run on the robot.
"""

# brickpi imports
from utils.brick import reset_brick, Motor
from utils.brick import wait_ready_sensors, EV3ColorSensor, TouchSensor, EV3UltrasonicSensor
from time import sleep
# function imports
from navigation import navigation

print("Start of program start.py.\nWaiting for sensors to turn on...")

# sensors and their ports
touch_sensor = TouchSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)
colorLeft = EV3ColorSensor(3)
colorRight = EV3ColorSensor(4)

# motors and their ports
motorRight = Motor("C")
motorLeft = Motor("D")

# delay between data samples
DELAY_SEC = 0.01

# initialize sensors, prints message when debug mode = True
wait_ready_sensors(True)

if __name__ == "__main__":
    navigation()
