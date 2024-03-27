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

'''
In progress: consistent left tunnel out behaviour
'''

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
        while us_sensor_side.get_cm()<23: # edit this value to figure out when sensor is in tunnel
            if us_sensor_side.get_cm()<= 6: # edit this value to adjust tolerance
                motorRight.set_power(-60)
                motorLeft.set_power(-20)
                print("adjust to move left")
                sleep(0.01)
            elif us_sensor_side.get_cm()>=8: # edit this value to adjust tolerance
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
            if (elapsed_time > 5):
                break # get out of while loop
        
        sleep(0.01)
        # out of the tunnel
        print("out of tunnel: go slighly left")
        if (us_sensor_side.get_cm() > 20): # if it passes through left tunnel
            motorRight.set_power(-45)
            motorLeft.set_power(-40)
            sleep(0.01)
        while (us_sensor_front.get_cm() > 25):
            print("moving to correct position")
        # make a sharp turn
        motorRight.set_power(-60) # 60 works when going through right tunnel
        motorLeft.set_power(60) # 20 works when going through left tunnel
        sleep(0.3) # edit this value to make sure most of the robot escapes the tunnel before proceeding
        print("done hard-coded portion")
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
    