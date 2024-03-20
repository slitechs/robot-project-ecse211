#!/usr/bin/env python3

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep
from utils.brick import Motor

DELAY_SEC = 0.01  # seconds of delay between measurements

print("Program start.\nWaiting for sensors to turn on...")

# Motors
motorRight = Motor("C")
motorLeft = Motor("D")

us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")

forward = True

def activate_ultrasonic():
    us_side_data = us_sensor_side.get_value()
    print(us_side_data)

if __name__ == "__main__":
    activate_ultrasonic()