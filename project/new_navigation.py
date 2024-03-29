#!/usr/bin/env python3

"""
Start: March 25, 2024
In Progress: March 26, 2024
In Progress: March 27, 2024
In Progress: March 29, 2024
"""

from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep, time
from tunnel_testing import inner_tunnel

print("Program start.\nWaiting for sensors to turn on...")

# this is where the I/O devices are accessed 
# TODO: is this needed when running from start? (needed for variable assignments, could use global vars instead?)
motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

DELAY_SEC = 0.01

wait_ready_sensors(True)
print("Done waiting")
forwardFacing = True
tunnel1 = False
red1 = False
backward = False
approaching_loading = False

def navigation():
    global forwardFacing
    try:
        print("Start navigation")
        
        while True:
            activate_ultrasonic()
            sleep(DELAY_SEC)
            get_color()   
            sleep(DELAY_SEC)
    except BaseException as e:
        print(e)
        motorRight.set_power(0)
        motorLeft.set_power(0)
    finally:
        print("Done navigation")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

def red_detected(r_rgb_data, l_rgb_data):
    if r_rgb_data[0] > r_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2] and l_rgb_data[0] > l_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2]:
        return True
    else:
        return False
    '''
    TODO: slow down 1 motor if crooked
    elif r_rgb_data[0] > r_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2]: # right only
        motorLeft.set_power(-10) # slow down left motor
        motorRight.set_power(0) # stop right motor
        sleep(0.01)
        return False
    elif l_rgb_data[0] > l_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2]: # left only
        motorLeft.set_power(0) # stop left motor
        motorRight.set_power(-10) # slow down right motor
        sleep(0.01)
        return False
    '''

def get_color():
    global red1
    global backward
    global approaching_loading
    if approaching_loading == False:
        color_data_r = colorRight.get_red() # list of float values
        color_data_l = colorLeft.get_red() # list of float values
        color_data_r_rgb = None
        color_data_l_rgb = None
    else:
        print("approaching loading, switched to get rgb")
        # TODO: determine if rgb needed for red
        color_data_r_rgb = colorRight.get_rgb()
        color_data_l_rgb = colorLeft.get_rgb()
        color_data_r = None
        color_data_l = None
    
    if ((color_data_l is not None and color_data_r is not None) or (color_data_l_rgb is not None and color_data_r_rgb is not None)) and forwardFacing == True: # if None then data collection failed so ignore
        # * For testing purposes
        #print("R: "+str(color_data_r) + " L: "+str(color_data_l))
        
        if approaching_loading == False and color_data_r + 20 < color_data_l and backward == False:
            # if right side sees black line
            # lessen right motor power
            motorRight.set_power(-20)
            motorLeft.set_power(-70)
            print("color-right")
            sleep(0.01)
        elif approaching_loading == False and color_data_l + 20< color_data_r and backward == False:
            # if left side sees black line
            # lessen left motor power
            motorRight.set_power(-70)
            motorLeft.set_power(-20)
            print("color-left")
            sleep(0.01)
        elif approaching_loading == False and backward == False:
            motorRight.set_power(-40)
            motorLeft.set_power(-40)
            print("color-both")
            sleep(0.01)

        # RED DETECTION: make sure robot is positioned straight when stopped
        
        # First time detecting red
        if approaching_loading == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red1 == False:
            print("RED DETECTED")
            red1 = True
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            sleep(0.01)
            # TODO: here, could slow down the robot?
            # TODO: polling US in color
            while US_SENSOR.get_cm() > 5: # change this value based on how close the sensor should get from the wall
                pass
            # stop the robot
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            # signal load ready
            print("signal loading ready")
            # TODO: flap catapult? Ask Mel & Emily
            # wait for physical signal to begin again
            # TODO: fix (polling ultrasonic in color...)
            while us_sensor_side.get_cm() is None or us_sensor_side.get_cm() > 1: # or != 255?
                pass
            # move backwards until it sees red
            motorLeft.set_power(30)
            motorRight.set_power(30)
            sleep(0.01)
            # TODO: even if it misses (for some reason), code it to turn around after a certain amount of seconds?
            while True:
                color_data_r_rgb = colorRight.get_rgb()
                color_data_l_rgb = colorLeft.get_rgb()
                if red_detected(color_data_r_rgb, color_data_l_rgb) == True:
                    motorRight.set_power(70) # adjustable
                    motorLeft.set_power(-70)
                    sleep(0.82) # adjust this to turn 180 degrees
                    # move forwards
                    motorRight.set_power(-40)
                    motorLeft.set_power(-40)
                    sleep(0.01)
                    approaching_loading = False
                    return
                
                """
                elif : # only right side red
                    motorLeft.set_power(-10) # slow down left motor
                    motorRight.set_power(0) # stop right motor
                    sleep(0.01)
                elif : # only left side red
                    motorLeft.set_power(0) # stop left motor
                    motorRight.set_power(10) # slow down right motor
                    sleep(0.01)
                """
                
        # Second time detecting red
        elif approaching_loading == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red1 == True:
            # turn 90 degrees right
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.5)
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.4) # edit this value based on robot design to do a 90 degree turn
            # move forward to shoot
            motorLeft.set_power(-30)
            motorRight.set_power(-30)
            sleep(0.5) # edit this value to make it move forward a certain amount - can also try to use front ultrasonic to detect distance to first bin
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.01)
            # shoot balls
            print("DONE ALL NAVIGATION")
            # TODO: this should return, and navigate to catapult code
            # return
            # TODO: this is for testing purposes only, get rid of it once the above (system) is integrated
            reset_brick() # Turn off everything on the brick's hardware, and reset it
            exit()

        
            
        
def activate_ultrasonic():
    global forwardFacing
    global tunnel1
    global approaching_loading
    try:
        us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
        us_side_data = us_sensor_side.get_value()

        if us_data is not None and us_side_data is not None: # If None is given, then data collection failed that time
            print("Front: "+str(us_data))
            print("Side: "+str(us_side_data))
            
            if forwardFacing == True and us_data <= 30 and tunnel1 == True and us_data != 0:
                motorRight.set_power(20)
                motorLeft.set_power(20)
                print("approaching loading true")
                approaching_loading = True
            #TODO: test this case where robot is coming back and needs to turn right before checking tunnels
            # ! make sure this is not activated when robot moves to loading zone (red)
            if forwardFacing == True and us_data <= 15 and tunnel1 == True and us_data!=0:
                print("wall detected, turning right to face tunnels")
                # stop moving
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(0.5)
                # turn right
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.4) # edit this value based on robot design to do a 90 degree turn
                # move forwards slowly
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                tunnel1 = False # reset tunnel variable


            # check if robot is too close in front (within 10 cm)
            if forwardFacing == True and us_data <= 10 and us_data != 0 and tunnel1 == False: # 0 was found to be a common value for noise, so need to disregard it (until filter is applied)
                print("forward facing and tunnel detected")
                # stop moving
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                # turn left (side ultrasonic is on right side)
                motorRight.set_power(-60)
                motorLeft.set_power(60)
                sleep(0.4) # edit this value based on robot design to do a 90 degree turn
                # move forwards slowly
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                forwardFacing = False
                print("forwardFacing = false now")
                sleep(0.5) # edit this duration to determine how long to move forwards for when checking the first (top) tunnel
                # ? TODO: check where this returns to (not sure if this is needed...this might be messing it up)
                #return
            
            if forwardFacing == False and us_side_data>50 and tunnel1 == False: # open tunnel detected
                # open tunnel is the one on the left
                print("nothing ahead detected, turn and go through tunnel")
                sleep(0.75) # buffer to make it go a bit farther before turning
                # stop
                motorLeft.set_power(0)
                motorRight.set_power(0)
                sleep(1)
                # turn right
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.4) # edit this value based on robot design to do a 90 degree turn
                # move forwards slowly
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                forwardFacing = True
                print("forwardFacing = true now")
                sleep(1.5) # change this to determine how long to wait until entire side ultrasonic sensor enters tunnel
                inner_tunnel() # activate tunnelling
                tunnel1 = True # mark tunnel as tunnelled
                # ? TODO: figure out whether this return is needed (previous testing shows that it seems to work)
                return
            elif forwardFacing == False and us_side_data < 20 and tunnel1 == False: # blocked tunnel detected
                print("blocked tunnel detected")
                # stop
                motorLeft.set_power(0)
                motorRight.set_power(0)
                sleep(1)
                 # move backwards slowly
                motorRight.set_power(30)
                motorLeft.set_power(30)
                
                # open tunnel is the one on the right
                while True:
                    # get more data
                    us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
                    us_side_data = us_sensor_side.get_value()

                    if forwardFacing == False and us_side_data>50: # open tunnel detected
                        print("nothing ahead detected, turn and go through tunnel")
                        sleep(0.15) # buffer to make it go a bit farther before turning
                        # stop
                        motorLeft.set_power(0)
                        motorRight.set_power(0)
                        sleep(1)
                        # turn right
                        motorRight.set_power(60)
                        motorLeft.set_power(-60)
                        sleep(0.37) # edit this value based on robot design to do a 90 degree turn
                        # move forwards slowly
                        motorRight.set_power(-30)
                        motorLeft.set_power(-30)
                        forwardFacing = True
                        print("forwardFacing = true now")
                        sleep(1) # change this to determine how long to wait until entire side ultrasonic sensor enters tunnel
                        inner_tunnel() # activate tunnelling
                        tunnel1 = True # mark tunnel as tunnelled
                        return
                    
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



