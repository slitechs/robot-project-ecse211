#!/usr/bin/env python3

"""
This file is used to plot RGB data collected from the color sensor.
It should be run on your computer, not on the robot.

Before running this script for the first time, you must install the dependencies
as explained in the README.md file.
"""

from ast import literal_eval
from math import sqrt, e, pi
from statistics import mean, stdev

from matplotlib import pyplot as plt
import numpy as np


COLOR_SENSOR_DATA_FILE = "./apr_4_tests/color_sensor_blue_l.csv"
output = "cs_l_blue.csv"

red, green, blue = [], [], []
with open(COLOR_SENSOR_DATA_FILE, "r") as f:
    for line in f.readlines():
        r, g, b = literal_eval(line)  # convert string to 3 floats
        # normalize the values to be between 0 and 1

        ### RATIO METHOD ###
        denominator = r + g + b
        if(r != 0 or g!=0 or b!= 0):
            red.append(r / denominator)
            green.append(g / denominator)
            blue.append(b / denominator)

output_file = open(output, "w")
for i in range(len(red)):
    output_file.write(f"{red[i]},{green[i]},{blue[i]}\n")








