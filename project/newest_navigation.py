#!/usr/bin/env python3

'''
Apr 4, 2024
Apr 7, 2024
'''

from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep, time
from tunnel_testing import inner_tunnel
from signal_load import signalf
from color_classification import classify_left, classify_right
import traceback

print("Program start.\nWaiting for sensors to turn on...")

# this is where the I/O devices are accessed 
# TODO: is this needed when running from start? (needed for variable assignments, could use global vars instead?)
catapult = Motor("B")
motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

DELAY_SEC = 0.01

wait_ready_sensors(True)
print("Done waiting")
forwardFacing = True # entering tunnel
tunnel1 = False # mark first time tunnel entered
tunnel2 = False # mark 2nd time tunnel entered
red1 = False # first time red detected
red2 = False # second time red detected
red3 = False # third time red detected
backward = False # robot is moving backward
approaching_loading = False # robot is approaching loading zone
loading = False # loading in progress
approaching_launch = False # robot is approaching launching zone
tunnel_distance = 35 # forwards distance from right tunnel coming back
wall_following = False
red_launch = False

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
# Red detection w/o classification
def red_detected(r_rgb_data, l_rgb_data):
    # TODO: change this to red color classification case
    if r_rgb_data[0] > r_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2] and l_rgb_data[0] > l_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2]:
        return True
    else:
        return False
    # TODO: stop 1 motor and move the other slowly if only 1 sensor detected red (to position the robot straight)
# Polls color sensor data
def get_color():
    global red1
    global red2
    global red3
    global backward
    global approaching_loading
    global loading
    global approaching_launch
    global wall_following
    global red_launch
    # Pick which type of value to sample
    if approaching_loading == False and approaching_launch == False:
        color_data_r = colorRight.get_red() # list of float values
        color_data_l = colorLeft.get_red() # list of float values
        color_data_r_rgb = None
        color_data_l_rgb = None
    else:
        print("loading/launching-related, get rgb")
        color_data_r_rgb = colorRight.get_rgb()
        color_data_l_rgb = colorLeft.get_rgb()
        color_data_r = None
        color_data_l = None
    # Check if data is valid
    if ((color_data_l is not None and color_data_r is not None) or (color_data_l_rgb is not None and color_data_r_rgb is not None)) and forwardFacing == True: # if None then data collection failed so ignore
        # * For testing purposes:
        #print("R: "+str(color_data_r) + " L: "+str(color_data_l))
        # STRAIGHT-LINE MOVEMENT FORWARDS
        # Check if get_red is used
        if color_data_r is not None and color_data_l is not None:
            if approaching_loading == False and color_data_r + 20 < color_data_l and backward == False:
                # if right side sees black line, lessen right motor power
                motorRight.set_power(-20)
                motorLeft.set_power(-70)
                print("color-right")
                sleep(0.01)
            elif approaching_loading == False and color_data_l + 20< color_data_r and backward == False:
                # if left side sees black line, lessen left motor power
                motorRight.set_power(-70)
                motorLeft.set_power(-20)
                print("color-left")
                sleep(0.01)
            elif approaching_loading == False and backward == False:
                motorRight.set_power(-40)
                motorLeft.set_power(-40)
                print("color-both")
                sleep(0.01)
            # STRAIGHT LINE MOVEMENT BACKWARDS
            '''
            if approaching_loading == False and color_data_r + 20 < color_data_l and backward == True:
                # if right side sees black line, lessen right motor power
                motorRight.set_power(20)
                motorLeft.set_power(60)
                print("color-right")
                sleep(0.01)
            elif approaching_loading == False and color_data_l + 20< color_data_r and backward == True:
                # if left side sees black line, lessen left motor power
                motorRight.set_power(20)
                motorLeft.set_power(60)
                print("color-left")
                sleep(0.01)
            '''
            if approaching_loading == False and backward == True:
                motorRight.set_power(30)
                motorLeft.set_power(30)
                print("color-both")
                sleep(0.01)
        # RED DETECTION
        # First time detecting red (into the loading zone)
        if approaching_loading == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red1 == False:
            print("RED DETECTED")
            red1 = True
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # turn 180 degrees
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.85) # adjust this value
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # move backwards
            motorRight.set_power(30)
            motorLeft.set_power(30)
            sleep(0.01)
        # Second time detecting red - stop
        elif approaching_loading == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red1 == True and red2 == False:
                print("red2 detected: stop")
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(0.01)
                approaching_loading = False
                red2 = True
                # loading mode
                loading = True
                return
        # Third time detecting red (before launching)
        elif approaching_launch == True and red_launch == True and red1 == True and red2 == True and red3 == False:
            print("red3 detected")
            # turn 90 degrees right
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.5)
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.4) # edit this value based on robot design to do a 90 degree turn
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(3)
            # shoot balls
            print("DONE ALL NAVIGATION")
            # TODO: this should return, and go to catapult code
            # return
            # TODO: this is for testing purposes only, get rid of it once the above (system) is integrated
            reset_brick() # Turn off everything on the brick's hardware, and reset it
            exit()
        # RGB NAVIGATION WITH COLOR CLASSIFICATION
        # TODO: this is copy-pasted from get_red
        if color_data_r_rgb is not None and color_data_l_rgb is not None:
            if approaching_loading == False and classify_right(color_data_r_rgb) == "red" and classify_left(color_data_l_rgb) == "red" and backward == False and approaching_launch == True:
                # both sensors detect red
                print("red detected using rgb")
                # stop robot
                motorRight.set_power(0)
                motorLeft.set_power(0)
                print("color-RED")
                red_launch = True
                sleep(1)
            elif approaching_loading == False and classify_right(color_data_r_rgb) == "black" and classify_left(color_data_l_rgb) == "blue" and backward == False:
                # if only right side sees black line, lessen right motor power
                motorRight.set_power(-20)
                motorLeft.set_power(-70)
                print("color-right")
                sleep(0.01)
            elif approaching_loading == False and classify_right(color_data_r_rgb) == "blue" and classify_left(color_data_l_rgb) == "black" and backward == False:
                # if only left side sees black line, lessen left motor power
                motorRight.set_power(-70)
                motorLeft.set_power(-20)
                print("color-left")
                sleep(0.01)
            elif approaching_loading == False and backward == False:
                motorRight.set_power(-40)
                motorLeft.set_power(-40)
                print("color-both")
                sleep(0.01)
# Polls ultrasonic sensor data
def activate_ultrasonic():
    global forwardFacing
    global tunnel1
    global tunnel2
    global approaching_loading
    global red1
    global red2
    global red3
    global backward
    global loading
    global approaching_launch
    global tunnel_distance
    global wall_following
    # Get data
    us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
    us_side_data = us_sensor_side.get_value()
    # Check if data is valid
    if us_data is not None and us_side_data is not None:
        # * For debugging
        # print("Front: "+str(us_data))
        # print("Side: "+str(us_side_data))
        # LOADING
        # In position to load
        if loading == True and red1 == True and red2 == True and red3 == False:
            # signal load ready
            print("signal loading ready. put hand on side sensor to reactivate robot")
            signalf()
            sleep(0.01)
            # wait for physical signal to begin again
            while us_sensor_side.get_cm() is None or us_sensor_side.get_cm() > 3: # or != 255?
                pass
            # no longer loading - update variables
            approaching_loading = False
            loading = False
            sleep(0.5)
            # reactivate color sensors
            colorRight.get_red()
            colorLeft.get_red()
            sleep(0.01)
            # move forwards
            motorLeft.set_power(-30)
            motorRight.set_power(-30)
            sleep(0.01)
            return
        # Approaching loading zone - detect wall
        if forwardFacing == True and us_data <= 16 and tunnel1 == True and red1 == False and red2 == False and us_data != 0:
            print("loading zone wall detected?: move backwards until in position")
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            if US_SENSOR.get_cm() > 16:
                # verify value
                return
            # move backwards
            motorRight.set_power(33)
            motorLeft.set_power(33)
            sleep(0.01)
            approaching_loading = True
        # ROUTE PT 2 - TUNNEL ENTERING
        # turn right to face tunnels (tunnel to go through is saved from 1st time)
        if forwardFacing == True and backward == True and us_data >= tunnel_distance and tunnel1 == True and red1 == True and red2 == True and us_data != 0:
            # stop and turn right to face tunnel
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.5)
            print("here")
            if tunnel_distance == 12:
                # right turn angle for left tunnel
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.38) # edit this value based on robot design to do a 90 degree turn right
            else:
                # right turn angle for right tunnel
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.46) # edit this value based on robot design to do a 90 degree turn right
            # stop
            motorLeft.set_power(0)
            motorRight.set_power(0)
            sleep(0.5)
            backward = False
            # move forwards slowly
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            sleep(3) # however long it might take to go thru tunnel
            inner_tunnel()
            forwardFacing = True
            print("start of out of tunnel")
            #sleep(0.1) # get entire robot body out of tunnel
            # TODO: this is for testing only
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # ! TODO: untested
            if tunnel_distance != 12:
                print("R tunnel out")
                motorRight.set_power(-30)
                motorLeft.set_power(0)
                sleep(1.3)
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                motorRight.set_power(-60)
                motorLeft.set_power(-30)
                sleep(0.01)
            else:
                print("L tunnel out")
                motorRight.set_power(-35)
                motorLeft.set_power(-40)
                sleep(0.01)
            print("robot starts moving again")
            # let robot reposition onto line for 5 seconds
            time_start = time()
            time_elapsed = 0
            while time_elapsed < 6:
                print("getred")
                get_color()
                sleep(0.01)
                time_end = time()
                time_elapsed = time_end-time_start
            approaching_launch = True
            print("switch to get rgb")
            tunnel2 = True
            return
        if forwardFacing == True and us_data <= 12 and tunnel2 == False and tunnel1 == True and red1 == True and red2 == True and us_data != 0:
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            print("at tunnels?")
            check_if_at_tunnels = US_SENSOR.get_cm()
            # check if it's actually true
            loop_index = 0
            while (check_if_at_tunnels is None) or (check_if_at_tunnels > 12 and loop_index < 5):
                # verify value
                check_if_at_tunnels = US_SENSOR.get_cm()
                sleep(0.5)
                print(check_if_at_tunnels)
                loop_index += 1
            print("at tunnels.")
            print(check_if_at_tunnels)
            if tunnel_distance > 12:
            # move backwards
                motorRight.set_power(30)
                motorLeft.set_power(30)
                sleep(0.01) 
            else:
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(0.01)
            backward = True
            return
        # ROUTE PT 1 - TUNNEL ENTERING
        # check if robot is close in front of tunnels (within 12 cm)
        if forwardFacing == True and us_data <= 13 and us_data != 0 and tunnel1 == False: # 0 was found to be a common value for noise, so need to disregard it
            print("forward facing and tunnel detected")
            # stop moving
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # turn left (side ultrasonic is on right side)
            motorRight.set_power(-60)
            motorLeft.set_power(60)
            sleep(0.45) # edit this value based on robot design to do a 90 degree turn
            # move forwards slowly
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            forwardFacing = False
            print("forwardFacing = false now")
            sleep(0.4) # edit this duration to determine how long to move forwards for when checking the first (top) tunnel 
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            return     
        # Left tunnel open, detected
        if forwardFacing == False and us_side_data > 40 and tunnel1 == False and us_side_data != 0:
            print("nothing ahead detected, turn and go through tunnel")
            motorLeft.set_power(-30)
            motorRight.set_power(-30)
            sleep(0.7) # untested: buffer to make it go a bit farther before turning
            # stop
            motorLeft.set_power(0)
            motorRight.set_power(0)
            sleep(1)
            # turn right
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.43) # edit this value based on robot design to do a 90 degree turn
            # move forwards slowly
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            forwardFacing = True
            print("forwardFacing = true now")
            sleep(2) # change this to determine how long to wait until entire side ultrasonic sensor enters tunnel
            inner_tunnel() # activate tunnelling
            # Out of tunnel
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # wall follow
            dist_from_wall = us_sensor_side.get_cm()
            print(dist_from_wall)
            while dist_from_wall < 30:
                print("adjust to be straight")
                # robot is facing right
                # turn it back straight
                motorRight.set_power(-30)
                motorLeft.set_power(30)
                sleep(0.01)
                dist_from_wall = us_sensor_side.get_cm()
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            while US_SENSOR.get_cm() is None or US_SENSOR.get_cm()>21 or US_SENSOR.get_cm()==0: # edit this value to figure out when sensor is in tunnel
                if us_sensor_side.get_cm()< dist_from_wall: # edit this value to adjust tolerance
                    motorRight.set_power(-40)
                    motorLeft.set_power(-30)
                    print("adjust to move left")
                    sleep(0.01)
                elif us_sensor_side.get_cm()>dist_from_wall: # edit this value to adjust tolerance
                    motorRight.set_power(-30)
                    motorLeft.set_power(-40)
                    print("adjust to move right")
                    sleep(0.01)
                else: 
                    print("go straight")
                    motorRight.set_power(-30)
                    motorLeft.set_power(-30)
                    sleep(0.01)
            print("front distance reached")
            print(US_SENSOR.get_cm())       
            sleep(0.01)
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.5)
            # turn left
            motorLeft.set_power(60)
            motorRight.set_power(-60)
            sleep(0.425) # adjust this to make a 90 degree turn
            # check distance from side wall
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            check_side_val = us_sensor_side.get_cm()
            print(check_side_val)
            while check_side_val is None or (check_side_val != 0 and check_side_val < 19):
                # turn left more
                print("left adjusting")
                motorRight.set_power(-35)
                motorLeft.set_power(-30)
                sleep(0.01)
                check_side_val = us_sensor_side.get_cm()
            while check_side_val is None or (check_side_val != 0 and check_side_val > 25):
                # turn right more
                print("right adjusting")
                motorRight.set_power(-30)
                motorLeft.set_power(-35)
                sleep(0.01)
                check_side_val = us_sensor_side.get_cm()
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            # move straight
            motorLeft.set_power(-40)
            motorRight.set_power(-40)
            sleep(1)
            tunnel1 = True # mark tunnel as tunnelled
            return
        # Right tunnel open, left tunnel detected as blocked
        elif forwardFacing == False and us_side_data < 20 and tunnel1 == False: # blocked tunnel detected
            print("blocked tunnel detected")
            # stop
            motorLeft.set_power(0)
            motorRight.set_power(0)
            sleep(1)
            # move backwards slowly
            motorRight.set_power(30)
            motorLeft.set_power(30)
            sleep(0.01)
            # open tunnel is the one on the right
            tunnel_distance = 12
            sleep(1.7) # make it move backwards
            # stop
            motorLeft.set_power(0)
            motorRight.set_power(0)
            sleep(1)
            # turn right
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.45) # edit this value based on robot design to do a 90 degree turn
            # move forwards slowly
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            forwardFacing = True
            print("forwardFacing = true now")
            sleep(1) # change this to determine how long to wait until entire side ultrasonic sensor enters tunnel
            inner_tunnel() # activate tunnelling
            # Out of tunnel
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # wall follow
            dist_from_wall = us_sensor_side.get_cm()
            print(dist_from_wall)
            while US_SENSOR.get_cm() is None or US_SENSOR.get_cm()>20 or US_SENSOR.get_cm()==0: # edit this value to figure out when sensor is in tunnel
                if us_sensor_side.get_cm()< dist_from_wall: # edit this value to adjust tolerance
                    motorRight.set_power(-40)
                    motorLeft.set_power(-30)
                    print("adjust to move left")
                    sleep(0.01)
                elif us_sensor_side.get_cm()>dist_from_wall: # edit this value to adjust tolerance
                    motorRight.set_power(-30)
                    motorLeft.set_power(-40)
                    print("adjust to move right")
                    sleep(0.01)
                else: 
                    print("go straight")
                    motorRight.set_power(-30)
                    motorLeft.set_power(-30)
                    sleep(0.01)
            print("front distance reached")
            print(US_SENSOR.get_cm())       
            sleep(0.01)
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.5)
            # turn left
            motorLeft.set_power(60)
            motorRight.set_power(-60)
            sleep(0.4) # adjust this to make a 90 degree turn
            # move straight
            motorLeft.set_power(-40)
            motorRight.set_power(-40)
            sleep(1)
            tunnel1 = True # mark tunnel as tunnelled
            return      
    sleep(DELAY_SEC)
if __name__ == "__main__":
    navigation()