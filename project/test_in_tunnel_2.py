from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.brick import reset_brick, EV3UltrasonicSensor
from time import sleep, time
import traceback

print("Program start.\nWaiting for sensors to turn on...")

door = Motor("A")
catapult = Motor("B")
motorRight = Motor("C")
motorLeft = Motor("D")
colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)
us_sensor_side = EV3UltrasonicSensor(1)
US_SENSOR = EV3UltrasonicSensor(2)

tunnel_distance = 12
tunnel_2_entering = False
at_tunnels = False

wait_ready_sensors(True)
print("Done waiting")

def loop_through():
    try:
        motorRight.set_power(-40)
        motorLeft.set_power(-40)
        sleep(0.01)
        while True:
            test_in_tunnel_2()
            sleep(0.01)
    except BaseException as e:
        print(e)
        motorRight.set_power(0)
        motorLeft.set_power(0)
    finally:
        print("Done everything.")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

def test_in_tunnel_2():
    global tunnel_2_entering
    global at_tunnels
    global tunnel_distance
    us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
    us_side_data = us_sensor_side.get_value()
    # Check if data is valid
    if us_data is not None and us_side_data is not None:
        print(us_data)
        if us_data <= 14 and at_tunnels == False:
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
        elif tunnel_2_entering == True and us_data <= (tunnel_distance + 1) and us_data >= (tunnel_distance - 1):
            print("here")
            # stop and turn right to face tunnel
            motorLeft.set_power(0) # stop
            motorRight.set_power(0) # stop
            sleep(0.5)
            print("here")
            if tunnel_distance == 12:
                print("L")
                # right turn angle for left tunnel
                motorRight.set_power(60)
                motorLeft.set_power(-60)
                sleep(.5) # edit this value based on robot design to do a 90 degree turn right (.475 not enough,.476 too much,.48 too much)
            else:
                print("R")
                # right turn angle for right tunnel
                motorRight.set_power(50)
                motorLeft.set_power(-50)
                sleep(0.5) # edit this value based on robot design to do a 90 degree turn right (.49 too much, .48 barelu)
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
            print("switch to get rgb")
            tunnel_2_entering = False
            return  
    
if __name__ == "__main__":
    loop_through()