#!/usr/bin/env python3

"""
Test navigation & color sensor (stop when red is detected)
"""

from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep

print("Program start.\nWaiting for sensors to turn on...")

motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
touch_sensor = TouchSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)


DELAY_SEC = 0.01


wait_ready_sensors(True)
print("Done waiting")

# TODO: ultrasonic and color into separate functions
def navigation():
    try:
        print("Start navigation")
        
        while True:
            if touch_sensor.is_pressed():
                motorRight.set_power(-70)
                motorLeft.set_power(-70)
            
            # get ultrasonic data
            us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
            
            if us_data is not None: # If None is given, then data collection failed that time
                print(us_data)
            # check if robot is too close (within 20 cm)
            if us_data <= 20:
                # stop moving
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                # move backwards
                motorRight.set_power(70)
                motorLeft.set_power(70)
                sleep(2)

                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)

            color_data_r = colorRight.get_rgb() # list of float values
            color_data_l = colorLeft.get_rgb() # list of float values
    
            if color_data_r is not None: # if None then data collection failed so ignore
                    #print("R: "+str(color_data_r))
                    print("R: "+str(color_data_r) + " L: "+str(color_data_l))
                    
                    # check if red, if yes then stop and do a 180 turn
                    if (color_data_r[0] > color_data_r[1] and color_data_r[0] > color_data_r[2]):
                        motorRight.set_power(0)
                        motorLeft.set_power(0)
                        sleep(1)
                        motorRight.set_power(70)
                        motorLeft.set_power(-70)
                        sleep(5)
                        motorRight.set_power(0)
                        motorLeft.set_power(0)
                    
            sleep(DELAY_SEC)
    except BaseException:
        motorRight.set_power(0)
        motorLeft.set_power(0)
    finally:
        print("Done navigation")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    navigation()
