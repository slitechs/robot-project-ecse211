from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep

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
    if us_sensor_side.get_cm()<= 8: 
        motorRight.set_power(-60)
        motorLeft.set_power(-20)
        print("right")
        sleep(0.01)
    elif us_sensor_side.get_cm()>=12: 
        motorRight.set_power(-60)
        motorLeft.set_power(-20)
        print("right")
        sleep(0.01)
    else: 
        motorRight.set_power(-50)
        motorLeft.set_power(-50)
        sleep(0.01)

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
                motorRight.set_power(80)
                motorLeft.set_power(80)
                sleep(1)
                #Turn
                motorRight.set_power(-80)
                motorLeft.set_power(80)
                sleep(1)
                inner_tunnel()

            else: 
                #Turn 
                motorRight.set_power(-80)
                motorLeft.set_power(80)
                sleep(1)
                inner_tunnel()

    except BaseException:
        motorRight.set_power(0)
        motorLeft.set_power(0)

    finally:
        print("Done tunneling")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()