#!/usr/bin/env python3
'''
* UNUSED * (actual ultrasonic function is in new_navigation)
'''

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep
from utils.brick import Motor


DELAY_SEC = 0.01  # seconds of delay between measurements

print("Program start.\nWaiting for sensors to turn on...")

# Motors
motorRight = Motor("C")
motorLeft = Motor("D")

us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")

forward = True
tunnel1 = False


def activate_ultrasonic():
    global forward
    global tunnel1
    try:
        us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
        us_side_data = us_sensor_side.get_value()

        if us_data is not None and us_side_data is not None: # If None is given, then data collection failed that time
            print("Front: "+str(us_data))
            print("Side: "+str(us_side_data))
            #print("Forward: "+str(forward))
            # check if robot is too close in front (within 15 cm)
            if forward == True and us_data <= 15 and us_data != 0 and tunnel1 == False: # 0 was found to be a common value for noise, so need to disregard it (until filter is applied)
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
            
            if forward == False and us_side_data>50 and tunnel1 == False: # open tunnel detected
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
            elif forward == False and us_side_data < 15 and tunnel1 == False: # blocked tunnel detected
                print("blocked tunnel detected")
                # stop
                motorLeft.set_power(0)
                motorRight.set_power(0)
                sleep(1)
                 # move backwards slowly
                motorRight.set_power(30)
                motorLeft.set_power(30)
                sleep(1.5)
            
        
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