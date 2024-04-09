from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep, time
import traceback

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
        side_sensor_value = us_sensor_side.get_cm()
        sleep(0.01)
        while True:
            if side_sensor_value is None:
                continue
            elif side_sensor_value > 20:
                print("out of tunnel?")
                # stop and check
                motorRight.set_power(0)
                motorLeft.set_power(0)
                sleep(0.3)
                side_sensor_value = us_sensor_side.get_cm() # check again just in case
                if side_sensor_value > 20:
                    break
            else:
                if side_sensor_value is not None and side_sensor_value <= 7: # edit this value to adjust tolerance
                    print("adjust to move left")
                    motorRight.set_power(-50)
                    motorLeft.set_power(-20)
                    sleep(0.01)
                elif side_sensor_value is not None and side_sensor_value >=9: # edit this value to adjust tolerance
                    print("adjust to move right")
                    motorRight.set_power(-20)
                    motorLeft.set_power(-50)
                    sleep(0.01)
                else: 
                    print("go straight")
                    motorRight.set_power(-35)
                    motorLeft.set_power(-35)
                    sleep(0.01)
            end_time = time()
            elapsed_time = end_time-start_time
            print(elapsed_time)
            if (elapsed_time > 5):
                break # get out of while loop
            side_sensor_value = us_sensor_side.get_cm()
            sleep(0.01)
        sleep(0.01)
        # out of the tunnel
        print("out of tunnel: go straight-ish then turn left at line")
        print(us_sensor_side.get_cm())
        # used for left tunnel: make it go a bit more forward before trying to wall follow
        print("go straight")
        motorRight.set_power(-40)
        motorLeft.set_power(-40)
        sleep(0.5)
        print("L tunnel out")
        # tilt
        motorRight.set_power(-30)
        motorLeft.set_power (0)
        sleep(0.8)
        # stop
        motorRight.set_power(0)
        motorLeft.set_power (0)
        sleep(0.3)
        # straight
        motorRight.set_power(-30)
        motorLeft.set_power(-45)
        sleep(0.5)
    except BaseException:
        motorRight.set_power(0)
        motorLeft.set_power(0)
        print(traceback.format_exc())
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
    
