from utils.brick import Motor, wait_ready_sensors, EV3UltrasonicSensor, EV3ColorSensor, BP, reset_brick
import time
import threading
from time import sleep, time
from signal_load import signalf
from color_classification import classify_left, classify_right
from load_and_launch import first_bucket, second_bucket, third_bucket

catapult = Motor("B")
door = Motor("A")
motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)
wait_ready_sensors()
print("Ready")

forwardFacing = True # entering tunnel
tunnel1 = False # mark first time tunnel entered
tunnel2 = False # mark 2nd time tunnel entered
red1 = True # first time red detected
red2 = True # second time red detected
red3 = False # third time red detected
backward = False # robot is moving backward
approaching_loading = False # robot is approaching loading zone
loading = False # loading in progress
approaching_launch = True # robot is approaching launching zone
tunnel_distance = 35 # forwards distance from right tunnel coming back
wall_following = False
red_launch = False
approached = False
at_tunnels = False
tunnel_2_entering = False

DELAY_SEC = 0.01

initial_door_position = door.get_position() #get initial position
print(initial_door_position)
initial_catapult_position = catapult.get_position()
print(initial_catapult_position)

def navigation():
    try:
        print("Start navigation")
        while True:
            approaching()   
            sleep(DELAY_SEC)
    except BaseException as e:
        print(e)
        motorRight.set_power(0)
        motorLeft.set_power(0)
    finally:
        print("Done everything.")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()
def red_detected(r_rgb_data, l_rgb_data):
    if r_rgb_data[0] > r_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2] and l_rgb_data[0] > l_rgb_data[1] and l_rgb_data[0] > l_rgb_data[2]:
        return True
    else:
        return False
def approaching():
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
    #print("loading/launching-related, get rgb")
    color_data_r_rgb = colorRight.get_rgb()
    color_data_l_rgb = colorLeft.get_rgb()
    color_data_r = None
    color_data_l = None
    # Check if data is valid
    if ((color_data_l is not None and color_data_r is not None) or (color_data_l_rgb is not None and color_data_r_rgb is not None)) and forwardFacing == True: # if None then data collection failed so ignore
        # Third time detecting red (before launching)
        if approaching_launch == True and red_launch == True and red1 == True and red2 == True and red3 == False:
            print("red3 detected")
            # turn 90 degrees right
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.5)
            # move slighly forwards
            motorLeft.set_power(-30)
            motorRight.set_power(-30)
            sleep(1)
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.1)
            motorRight.set_power(60)
            motorLeft.set_power(-60)
            sleep(0.51) # edit this value based on robot design to do a 90 degree turn, initially=0.55
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(1)
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


if __name__ == "__main__":
    navigation()
    #first_bucket()
    #second_bucket()
    #third_bucket()

    

