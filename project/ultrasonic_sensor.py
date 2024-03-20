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

TOUCH_SENSOR = TouchSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")

# TODO: add median filter to filter out noise (255 and 0 values)
def activate_ultrasonic():
    try:
        us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
        if us_data is not None: # If None is given, then data collection failed that time
            print(us_data)
            # check if robot is too close (within 20 cm)
            if us_data <= 20 and us_data != 0: # 0 was found to be a common value for noise, so need to disregard it (until filter is applied)
                # stop moving
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                # move backwards
                motorRight.set_power(70)
                motorLeft.set_power(70)
                sleep(2)
                # move forwards
                motorRight.set_power(-70)
                motorLeft.set_power(-70)
                sleep(1)
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)

        sleep(DELAY_SEC)
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        print("Done collecting US distance samples")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

# applies filter of the specified length on input vector
def median_filter(input_vec, length):
    vector_length = len(input_vec)
    for i in range(vector_length - length):
        # sort numbers in increasing order
        sorted_vector = input_vec[i:i+length].sort()
        print("debugging median filter, sorted: "+sorted_vector)
        med_value = sorted_vector[length//2]
        if input_vec[i]>med_value:
            

            print("unfinished")
        

if __name__ == "__main__":
    activate_ultrasonic()