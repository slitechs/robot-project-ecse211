#!/usr/bin/env python3

"""
This test is used to collect data from 2 color sensors simultaneously.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor
from utils.brick import reset_brick
from time import sleep

#COLOR_SENSOR_DATA_FILE_R = "../data_analysis/color_sensor_right.csv"
#COLOR_SENSOR_DATA_FILE_L = "../data_analysis/color_sensor_left.csv"
COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
#TOUCH_SENSOR = TouchSensor(1)

DELAY_SEC = 0.01  # seconds of delay between color sensor samples

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("done")

def collect_color_sensor_data():
    "Collect color sensor data."
    try:
        print("start")
        # open output file
        output_file = open(COLOR_SENSOR_DATA_FILE, "w") # w for write
        # output_file_l = open(COLOR_SENSOR_DATA_FILE_L, "w") # w for write
        # data_points_collected = 0
        # continuously sample color sensor until 10 data points are collected
        # while data_points_collected < 10: # while True to continuously sample until an exception is detected (Ctrl-C, program exits)
        while True:
            color_data_r = colorRight.get_rgb() # list of float values
            color_data_l = colorLeft.get_rgb() # list of float values
    
            if color_data_r is not None: # if None then data collection failed so ignore
                    #print("R: "+str(color_data_r))
                    print("R: "+str(color_data_r) + " L: "+str(color_data_l))
                    output_file.write(f"R: {color_data_r} L: {color_data_l}\n") # write color sensor reading to output file

            sleep(DELAY_SEC)
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        print("Done collecting Color Sensor RGB samples")
        output_file.close()
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    collect_color_sensor_data()
