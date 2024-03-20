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

def navigation():
    try:
        print("Start navigation")
        turned = False
        
        while True:
            #if touch_sensor.is_pressed():
                
                #motorRight.set_power(-70)
                #motorLeft.set_power(-70)
            
            # get ultrasonic data
            #us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
            
            #if us_data is not None: # If None is given, then data collection failed that time
                #print(us_data)
                # check if robot is too close (within 20 cm)
                #if us_data <= 20 and us_data !=0:
                    # stop moving
                    #motorRight.set_power(0)
                    #motorLeft.set_power(0)
                    #sleep(1)
                    # move backwards
                    #motorRight.set_power(60)
                    #motorLeft.set_power(60)
                    #sleep(2)

                    # stop
                    #motorRight.set_power(0)
                    #motorLeft.set_power(0)

            color_data_r = colorRight.get_red() # list of float values # can be get_rgb or get_red
            color_data_l = colorLeft.get_red() # list of float values # can be get_rgb or get_red
            
            # red way
            if color_data_l is not None and color_data_r is not None: # if None then data collection failed so ignore
                    print("R: "+str(color_data_r) + " L: "+str(color_data_l))
                    
                    if (color_data_r + 20 < color_data_l):
                        # if right side sees black line
                        # lessen right motor power
                        motorRight.set_power(-40)
                        motorLeft.set_power(-90)
                        print("right")
                        sleep(0.01)
                    elif (color_data_l + 20< color_data_r):
                        # if left side sees black line
                        # lessen left motor power
                        motorRight.set_power(-90)
                        motorLeft.set_power(-40)
                        print("left")
                        sleep(0.01)
                    else:
                        motorRight.set_power(-80)
                        motorLeft.set_power(-80)
                        sleep(0.01)
                    
                    # rgb way
                    """
                    if (color_data_l[0] > color_data_l[1]+20 and color_data_l[0] > color_data_l[2]+20):
                        # check if red, if yes then stop and do a 180 turn
                        motorRight.set_power(0)
                        motorLeft.set_power(0)
                        sleep(1)
                        if turned == False:
                            motorRight.set_power(70)
                            motorLeft.set_power(-70)
                            sleep(0.82)
                            turned = True
                            print(turned)
                            motorRight.set_power(70)
                            motorLeft.set_power(70)
                            sleep(1)
                    elif (color_data_r[0] > color_data_r[1]+10 and color_data_r[0] > color_data_r[2]+10):
                        # check if red, if yes then stop and do a 180 turn
                        motorRight.set_power(0)
                        motorLeft.set_power(0)
                        sleep(1)
                        if turned == False:
                            motorRight.set_power(70)
                            motorLeft.set_power(-70)
                            sleep(0.82)
                            turned = True
                            print(turned)
                            motorRight.set_power(70)
                            motorLeft.set_power(70)
                            sleep(1)
                    elif color_data_r[0]<color_data_l[0]-20:
                        # if right side sees black line
                        # lessen right motor power
                        motorRight.set_power(-40)
                        motorLeft.set_power(-90)
                        sleep(0.01)
                    elif color_data_l[0]<color_data_r[0]-20:
                        # if left side sees black line
                        # lessen right motor power
                        motorLeft.set_power(-40)
                        motorRight.set_power(-90)
                        sleep(0.01)
                    else:
                        motorLeft.set_power(-80)
                        motorRight.set_power(-80)
                        sleep(0.01)
                    """
                    
                    
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
