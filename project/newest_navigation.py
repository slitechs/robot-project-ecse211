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
from load_and_launch import first_bucket, second_bucket, third_bucket

print("Program start.\nWaiting for sensors to turn on...")

# this is where the I/O devices are accessed 
# TODO: is this needed when running from start? (needed for variable assignments, could use global vars instead?)
door = Motor("A")
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

# Global variables
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
approached = False
at_tunnels = False
tunnel_2_entering = False

# Polling-based navigation
def navigation():
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
        print("Done everything.")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

# In some cases, the ultrasonic sensor gets incorrect values for a brief period. 
# This function is used to verify the data values from the ultrasonic sensor to ensure they are consistent.
# This is needed since the robot uses the ultrasonic sensors' values to determine its position while navigating.
def verify_value():
    print("verify ultrasonic sensor values")

# Red detection with get_red()
def red_detected(r_rgb_data, l_rgb_data):
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
    global forwardFacing
    # Pick which type of value to sample
    if approaching_loading == False and approaching_launch == False:
        color_data_r = colorRight.get_red() # list of float values
        color_data_l = colorLeft.get_red() # list of float values
        color_data_r_rgb = None
        color_data_l_rgb = None
    else:
        #print("loading/launching-related, get rgb")
        color_data_r_rgb = colorRight.get_rgb()
        color_data_l_rgb = colorLeft.get_rgb()
        color_data_r = None
        color_data_l = None
    # Check if data is valid
    if ((color_data_l is not None and color_data_r is not None) or (color_data_l_rgb is not None and color_data_r_rgb is not None)) and forwardFacing == True: # if None then data collection failed so ignore
        # * For testing purposes:
        #print("R: "+str(color_data_r) + " L: "+str(color_data_l))
        #print(motorRight.get_power())
        #print(motorLeft.get_power())
        # STRAIGHT-LINE MOVEMENT FORWARDS
        # Check if get_red is used
        if color_data_r is not None and color_data_l is not None:
            if approaching_loading == False and color_data_r + 20 < color_data_l and backward == False:
                # if right side sees black line, lessen right motor power
                motorRight.set_power(-20)
                motorLeft.set_power(-70)
                #print("color-right")
                sleep(0.01)
            elif approaching_loading == False and color_data_l + 20< color_data_r and backward == False:
                # if left side sees black line, lessen left motor power
                motorRight.set_power(-70)
                motorLeft.set_power(-20)
                #print("color-left")
                sleep(0.01)
            elif approaching_loading == False and backward == False:
                motorRight.set_power(-40)
                motorLeft.set_power(-40)
                #print("color-both")
                sleep(0.01)
            elif approaching_loading == False and backward == True:
                motorRight.set_power(30)
                motorLeft.set_power(30)
                #print("color-both")
                sleep(0.01)
        if color_data_l_rgb is not None and color_data_r_rgb is not None:
            # RED DETECTION
            # First time detecting red (into the loading zone)
            if approaching_loading == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red1 == False and red2 == False and red3 == False:
                print("RED DETECTED")
                red1 = True
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                # turn 180 degrees
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.9) # adjust this value
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                # move backwards
                motorRight.set_power(30)
                motorLeft.set_power(30)
                sleep(0.1)
                return
            # Second time detecting red - stop
            elif approaching_loading == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red1 == True and red2 == False and red3 == False:
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
            elif approaching_launch == True and red_detected(color_data_r_rgb, color_data_l_rgb) == True and red_launch == True and red1 == True and red2 == True and red3 == False:
                print("red3 detected")
                # turn 90 degrees right
                motorLeft.set_power(0) # stop
                motorRight.set_power(0) # stop
                sleep(0.1)
                # move slighly forwards
                motorLeft.set_power(-30)
                motorRight.set_power(-30)
                sleep(1)
                motorLeft.set_power(0) # stop
                motorRight.set_power(0) # stop
                sleep(0.1)
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(0.525) # edit this value based on robot design to do a 90 degree turn
                motorLeft.set_power(0) # stop
                motorRight.set_power(0) # stop
                sleep(0.1)
                # shoot balls
                print("DONE ALL NAVIGATION")
                # CATAPULT
                first_bucket()
                second_bucket()
                third_bucket()
                print("DONE ALL, BRICKPI OFF")
                reset_brick() # Turn off everything on the brick's hardware, and reset it
                exit()
            # RGB NAVIGATION WITH COLOR CLASSIFICATION
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
                print("rgb-right")
                sleep(0.01)
            elif approaching_loading == False and classify_right(color_data_r_rgb) == "blue" and classify_left(color_data_l_rgb) == "black" and backward == False:
                # if only left side sees black line, lessen left motor power
                motorRight.set_power(-70)
                motorLeft.set_power(-20)
                print("rgb-left")
                sleep(0.01)
            elif approaching_loading == False and backward == False:
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                print("rgb-both")
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
    global approached
    global at_tunnels
    global tunnel_2_entering
    # Get data
    us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
    us_side_data = us_sensor_side.get_value()
    # Check if data is valid
    if us_data is not None and us_side_data is not None:
        # FOR DEBUGGING
        # print("Front: "+str(us_data))
        #print("Side: "+str(us_side_data))
        # ROUTE PT 1 - TUNNEL ENTERING
        # check if robot is close in front of tunnels (within 12 cm)
        if forwardFacing == True and us_data <= 14 and us_data != 0 and tunnel1 == False: # 0 was found to be a common value for noise, so need to disregard it
            print("forward facing and tunnel detected?")
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            # verify
            v_index = 0
            while v_index<5:
                sleep(0.1)
                us_data = US_SENSOR.get_cm()
                if us_data is None:
                    continue
                elif us_data > 14:
                    return
                print(us_data)
                v_index += 1
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
            sleep(0.5) # edit this duration to determine how long to move forwards for when checking the first (top) tunnel 
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            forwardFacing = False
            print("forwardFacing = false now")
            return
        elif forwardFacing == False and us_side_data <= 30 and us_side_data >= 20 and tunnel1 == False:
            print("unsure")
            sleep(0.01)
        # Left tunnel open, detected
        elif forwardFacing == False and us_side_data > 30 and tunnel1 == False and us_side_data != 0:
            print("nothing ahead detected, turn and go through tunnel")
            motorLeft.set_power(-30)
            motorRight.set_power(-30)
            sleep(0.7)
            # stop
            motorLeft.set_power(0)
            motorRight.set_power(0)
            sleep(1)
            # turn right
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.52) # edit this value based on robot design to do a 90 degree turn (0.5 too little, 0.55 too much)
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
            # move straight
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            sleep(0.5)
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # turn kinda left
            motorRight.set_power(-30)
            motorLeft.set_power(0)
            sleep(.2)
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            # wall follow
            dist_from_wall = us_sensor_side.get_cm()
            print(dist_from_wall)
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            out_of_tunnls_us = US_SENSOR.get_cm()
            while True:
                out_of_tunnls_us = US_SENSOR.get_cm()
                if out_of_tunnls_us is None or out_of_tunnls_us == 0:
                    # stop
                    motorRight.set_power(0)
                    motorLeft.set_power(0)
                    sleep(0.01)
                    continue
                elif out_of_tunnls_us > 20:
                    # wall follow
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
                else:
                    motorRight.set_power(0)
                    motorLeft.set_power(0)
                    sleep(0.1)
                    # verify
                    out_of_tunnls_us = US_SENSOR.get_cm()
                    if out_of_tunnls_us is None or out_of_tunnls_us == 0:
                        return
                    elif out_of_tunnls_us <= 20:
                        break
                    else:
                        motorRight.set_power(-30)
                        motorLeft.set_power(-30)
                        sleep(0.1)
            print("front distance reached")
            print(out_of_tunnls_us)       
            sleep(0.01)
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.5)
            # turn left
            motorLeft.set_power(60)
            motorRight.set_power(-60)
            sleep(0.41) # adjust this to make a 90 degree turn
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.5)
            # move straight
            motorLeft.set_power(-40)
            motorRight.set_power(-40)
            sleep(1)
            tunnel1 = True # mark tunnel as tunnelled
            return
        # Right tunnel open, left tunnel detected as blocked
        elif forwardFacing == False and us_side_data < 20 and tunnel1 == False: # blocked tunnel detected
            print("blocked tunnel? verify in progress")
            # verify
            ver_index = 0
            while ver_index<5:
                sleep(0.1)
                us_side_data = us_sensor_side.get_cm()
                if us_side_data is None:
                    continue
                elif us_side_data > 20:
                    return
                print(us_side_data)
                ver_index += 1
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
            sleep(0.47) # edit this value based on robot design to do a 90 degree turn (EDITED)
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
            dist_from_front = US_SENSOR.get_cm()
            print(dist_from_wall)
            while True:
                dist_from_front = US_SENSOR.get_cm()
                if dist_from_front is None or dist_from_front == 0:
                    print("invalid value, try again")
                    # stop
                    motorRight.set_power(0)
                    motorLeft.set_power(0)
                    sleep(0.5)
                    continue
                elif dist_from_front<20:
                    # stop
                    motorRight.set_power(0)
                    motorLeft.set_power(0)
                    sleep(0.5)
                    # verify once
                    dist_from_front = US_SENSOR.get_cm()
                    if dist_from_front < 20:
                        break
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
            sleep(0.44) # adjust this to make a 90 degree turn
            # move straight
            motorLeft.set_power(-40)
            motorRight.set_power(-40)
            sleep(1)
            tunnel1 = True # mark tunnel as tunnelled
            return
        # LOADING
        # Approaching loading zone - detect wall
        if forwardFacing == True and us_data <= 16 and approached == False and tunnel1 == True and red1 == False and red2 == False and us_data != 0:
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            print("loading zone wall detected?: move backwards until in position")
            check_if_at_load = US_SENSOR.get_cm()
            # check if it's actually true
            loop_index_load = 0
            while loop_index_load < 5:
                if check_if_at_load is None:
                    continue
                elif check_if_at_load > 18:
                    return
                # verify value
                check_if_at_load = US_SENSOR.get_cm()
                sleep(0.1)
                print(check_if_at_load)
                loop_index_load += 1
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            if US_SENSOR.get_cm() > 16:
                # verify value
                return
            # move backwards
            motorRight.set_power(30)
            motorLeft.set_power(33)
            sleep(0.1)
            approaching_loading = True
            approached = True
            return
        # In position to load
        elif loading == True and red1 == True and red2 == True and red3 == False:
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
        # ROUTE PT 2 - TUNNEL ENTERING
        # sees wall ahead
        if forwardFacing == True and us_data <= 14 and at_tunnels == False and tunnel2 == False and tunnel1 == True and red1 == True and red2 == True and us_data != 0:
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(0.01)
            print("at tunnels pt 2?")
            check_if_at_tunnels = US_SENSOR.get_cm()
            # check if it's actually true
            loop_index = 0
            while loop_index < 5:
                print(check_if_at_tunnels)
                print("Loop index:" + str(loop_index))
                if check_if_at_tunnels is None or check_if_at_tunnels == 0:
                    continue
                elif check_if_at_tunnels > 15:
                    return
                # verify value
                check_if_at_tunnels = US_SENSOR.get_cm()
                loop_index += 1
                sleep(0.1)
            print("at tunnels pt 2.")
            print(check_if_at_tunnels)
            if tunnel_distance > 12:
            # move backwards slowly
                motorRight.set_power(30)
                motorLeft.set_power(33)
                sleep(0.01)
                backward = True
            else:
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(0.01)
                # move forwards slowly
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                sleep(0.01)
            tunnel_2_entering = True
            at_tunnels = True
            return  
        # turn right to face tunnels (tunnel to go through is saved from 1st time)
        elif forwardFacing == True and tunnel_2_entering == True and us_data <= (tunnel_distance + 1) and us_data >= (tunnel_distance - 1) and tunnel1 == True and red1 == True and red2 == True and us_data != 0:
            # stop and turn right to face tunnel
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.5)
            print("here")
            if tunnel_distance == 12:
                # right turn angle for left tunnel
                motorRight.set_power(50)
                motorLeft.set_power(-50)
                sleep(.59) # edit this value based on robot design to do a 90 degree turn right (.475 not enough,.476 too much,.48 too much)
            else:
                # right turn angle for right tunnel
                motorRight.set_power(50)
                motorLeft.set_power(-50)
                sleep(0.57) # edit this value based on robot design to do a 90 degree turn right (.51 not enough, .48 barelu)
            # stop
            motorLeft.set_power(0)
            motorRight.set_power(0)
            sleep(0.5)
            backward = False
            # move forwards slowly
            motorRight.set_power(-30)
            motorLeft.set_power(-30)
            sleep(3.5) # however long it might take to go thru tunnel
            inner_tunnel()
            forwardFacing = True
            print("start of out of tunnel")
            # stop
            motorRight.set_power(0)
            motorLeft.set_power(0)
            sleep(1)
            if tunnel_distance != 12:
                print("R tunnel out")
                #forwards so it doesnt get stuck
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                sleep(0.5)
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                motorRight.set_power(-30)
                motorLeft.set_power(0)
                sleep(0.3)
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                print("move forwards a bit")
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                sleep(1)
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                out_of_tunnel_us = US_SENSOR.get_cm()
                while True:
                    out_of_tunnel_us = US_SENSOR.get_cm()
                    print(out_of_tunnel_us)
                    if (out_of_tunnel_us is None):
                        # stop
                        motorRight.set_power(0)
                        motorLeft.set_power(0)
                        sleep(0.01)
                        out_of_tunnel_us = US_SENSOR.get_cm()
                        continue
                    elif (out_of_tunnel_us < 105 and out_of_tunnel_us >= 80):
                        # verify
                        # stop
                        motorRight.set_power(0)
                        motorLeft.set_power(0)
                        sleep(0.01)
                        out_of_tunnel_us = US_SENSOR.get_cm()
                        if out_of_tunnel_us < 105:
                            break
                    elif (out_of_tunnel_us < 80):
                        motorRight.set_power(0)
                        motorLeft.set_power(-30)
                        sleep(0.01)
                    elif (out_of_tunnel_us>=105):
                        print("adjust")
                        motorRight.set_power(-30)
                        motorLeft.set_power(0)
                        sleep(0.01)
                # stop
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(0.5)
                print("done adjusting, start")
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                sleep(0.01)
            else:
                print("L tunnel out")
                motorRight.set_power(-40)
                motorLeft.set_power(-40)
                sleep(1)
                motorRight.set_power(-30)
                motorLeft.set_power(0)
                sleep(0.3)
                front_dist_l_tunnel_out = US_SENSOR.get_cm()
                print(front_dist_l_tunnel_out)
                # tilt
                while True:
                    front_dist_l_tunnel_out = US_SENSOR.get_cm()
                    print(front_dist_l_tunnel_out)
                    if front_dist_l_tunnel_out is None:
                        # stop
                        motorRight.set_power(0)
                        motorLeft.set_power (0)
                        sleep(0.1)
                        continue
                    elif front_dist_l_tunnel_out > 40:
                        motorRight.set_power(-30)
                        motorLeft.set_power (0)
                        sleep(0.01)
                    else:
                        # stop
                        motorRight.set_power(0)
                        motorLeft.set_power (0)
                        sleep(0.1)
                        break
                # stop
                motorRight.set_power(0)
                motorLeft.set_power (0)
                sleep(0.3)
                print("front dist: "+str(front_dist_l_tunnel_out))
                # tilt
                motorRight.set_power(0)
                motorLeft.set_power (-30)
                sleep(1.77) #1.5 is too little, 1.7 looked like it barely worked, 1.8 too much
                print("done adjusting")
                # straight
                motorRight.set_power(-30)
                motorLeft.set_power(-30)
                sleep(2)
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
            tunnel_2_entering = False
            return  
    else:
        print("None value, try again")
if __name__ == "__main__":
    navigation()