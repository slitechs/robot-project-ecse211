#!/usr/bin/env python3

"""
Start: March 25, 2024
"""

from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep
from tunnel_testing import inner_tunnel

print("Program start.\nWaiting for sensors to turn on...")

# this is where the I/O devices are accessed 
# TODO: is this needed when running from start?
motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

DELAY_SEC = 0.01

wait_ready_sensors(True)
print("Done waiting")
forward = True

def navigation():
    global forward
    try:
        print("Start navigation")
        
        while True:
            activate_ultrasonic() # in tunnel is a boolean
            sleep(0.01)
            try:
                print(forward)
            except BaseException as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
                print(e)
                
            color_data_r = colorRight.get_red() # list of float values
            color_data_l = colorLeft.get_red() # list of float values
            
            if color_data_l is not None and color_data_r is not None: # if None then data collection failed so ignore
                    # * For testing purposes
                    #print("R: "+str(color_data_r) + " L: "+str(color_data_l))
                        
                    if (color_data_r + 20 < color_data_l):
                        # if right side sees black line
                        # lessen right motor power
                        motorRight.set_power(-20)
                        motorLeft.set_power(-70)
                        print("right")
                        sleep(0.01)
                    elif (color_data_l + 20< color_data_r):
                        # if left side sees black line
                        # lessen left motor power
                        motorRight.set_power(-70)
                        motorLeft.set_power(-20)
                        print("left")
                        sleep(0.01)
                    else:
                        motorRight.set_power(-40)
                        motorLeft.set_power(-40)
                        sleep(0.01)
                    
                    
            sleep(DELAY_SEC)
    except BaseException:
        motorRight.set_power(0)
        motorLeft.set_power(0)
    finally:
        print("Done navigation")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()
        
def activate_ultrasonic():
    global forward
    try:
        us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
        us_side_data = us_sensor_side.get_value()
        #def check_us_sensors(forward):
        if us_data is not None and us_side_data is not None: # If None is given, then data collection failed that time
            print("Front: "+str(us_data))
            print("Side: "+str(us_side_data))
            # TODO: print this for debugging once forward global variable works
            #print("Forward: "+str(forward))
            # check if robot is too close in front (within 20 cm)
            if forward == True and us_data <= 15 and us_data != 0: # 0 was found to be a common value for noise, so need to disregard it (until filter is applied)
                print("forwards and tunnel detected")
                # stop moving
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                # turn left (side ultrasonic is on right side)
                motorRight.set_power(-60)
                motorLeft.set_power(60)
                sleep(0.5) # edit this value based on robot design to do a 90 degree turn
                # move forwards slowly
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                forward = False
                print("forward = false now")
                sleep(1)
                return # get out of check_us_sensors
            
            if forward == False and us_side_data>50: # open tunnel detected
                print("nothing ahead detected, turn and go through tunnel")
                #sleep(0.4) # buffer to make it go a bit farther before turning
                # stop
                motorLeft.set_power(0)
                motorRight.set_power(0)
                sleep(1)
                # turn right
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.5) # edit this value based on robot design to do a 90 degree turn
                # move forwards slowly
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                forward = True
                print("forward = true now")
                sleep(1)
                return
            elif forward == False and us_side_data < 15: # blocked tunnel detected
                print("blocked tunnel detected")
                # stop
                motorLeft.set_power(0)
                motorRight.set_power(0)
                sleep(1)
                 # move backwards slowly
                motorRight.set_power(30)
                motorLeft.set_power(30)
                sleep(1.5)
            
        #check_us_sensors(forward)
        
        sleep(DELAY_SEC)
    except BaseException as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print(e)
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()
        pass
    finally:
        #print("Done collecting US distance samples")
        print("")
        #reset_brick() # Turn off everything on the brick's hardware, and reset it
        #exit()


if __name__ == "__main__":
    navigation()



