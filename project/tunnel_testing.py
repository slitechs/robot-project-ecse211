from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep, time

print("Program start.\nWaiting for sensors to turn on...")

motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
#touch_sensor = TouchSensor(1)
us_sensor_side = EV3UltrasonicSensor(1)
us_sensor_front = EV3UltrasonicSensor(2)


DELAY_SEC = 0.01


wait_ready_sensors(True)
print("Done waiting")

'''
Code for navigation inside the tunnel 
'''
def inner_tunnel():
    try:
        print("Start inner tunnel navigation")
        start_time = time()
        print("Time starts here")
        while us_sensor_side.get_cm()<20: # edit this value to figure out when sensor is in tunnel
            if us_sensor_side.get_cm()<= 6: # edit this value to adjust tolerance
                motorRight.set_power(-60)
                motorLeft.set_power(-20)
                print("adjust to move left")
                sleep(0.01)
            elif us_sensor_side.get_cm()>=9: # edit this value to adjust tolerance
                motorRight.set_power(-20)
                motorLeft.set_power(-60)
                print("adjust to move right")
                sleep(0.01)
            else: 
                print("go straight")
                motorRight.set_power(-40)
                motorLeft.set_power(-40)
                sleep(0.01)
            end_time = time()
            elapsed_time = end_time-start_time
            print(elapsed_time)
            if (elapsed_time > 4.7):
                break # get out of while loop
        
        sleep(0.01)
        # out of the tunnel 
        print("out of tunnel: go straight then turn left at line")
        motorRight.set_power(-30) # (other way: 60 works when going through right tunnel)
        motorLeft.set_power(-30) # (20 works when going through right tunnel)
        sleep(0.01) # edit this value to make sure most of the robot escapes the tunnel before proceeding
        while us_sensor_front.get_cm()>35: # check distance from wall
            pass # keep moving forward
        print("distance from wall to line reached")
        # stop
        motorRight.set_power(0)
        motorLeft.set_power(0)
        sleep(0.5)
        # turn left
        motorLeft.set_power(50)
        motorRight.set_power(-50)
        sleep(0.3) # adjust this to make a 90 degree turn
        # move straight
        motorLeft.set_power(-40)
        motorRight.set_power(-40)
        sleep(1.7)
        # turn left
        motorLeft.set_power(50)
        motorRight.set_power(-50)
        sleep(0.25) # adjust this to make a 90 degree turn
        # move straight
        motorLeft.set_power(-40)
        motorRight.set_power(-40)
        sleep(0.01)
        # wall following
        '''
        side_value = us_sensor_side.get_cm()
        if side_value > 20:
            print("> 20")
            while us_sensor_side.get_cm() > 15:
                motorLeft.set_power(-40)
                motorRight.set_power(-30)
                sleep(0.01)
        elif side_value < 15:
            print("< 15")
            while us_sensor_side.get_cm() < 15:
                motorLeft.set_power(-30)
                motorRight.set_power(-40)
                sleep(0.01)
        '''
        # move straight
        motorLeft.set_power(-40)
        motorRight.set_power(-40)
        sleep(0.01)        
            
    except BaseException:
        motorRight.set_power(0)
        motorLeft.set_power(0)
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()
        
    finally:
        print("Done inner_tunnel")

'''
Code to detect if tunnel is blocked 
'''
def tunnel():
    try:
        print("Start navigation")
        turned = False

        while True:
            #Check if the furthest tunnel is blocked
            if us_sensor_side.get_cm() <= 10: 
                #Go back to the second tunnel 
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(1)
                #Turn
                motorRight.set_power(-0)
                motorLeft.set_power(0)
                sleep(1)
                inner_tunnel()

            else: 
                #Turn 
                motorRight.set_power(-0)
                motorLeft.set_power(0)
                sleep(1)
                inner_tunnel()

    except BaseException:
        motorRight.set_power(0)
        motorLeft.set_power(0)
        

    finally:
        print("Done tunneling")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    inner_tunnel()
    