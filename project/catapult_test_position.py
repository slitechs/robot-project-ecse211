from utils.brick import Motor, TouchSensor, wait_ready_sensors, BP  
import time

#motor = Motor("A")
catapult = Motor("B")
TOUCH_SENSOR = TouchSensor(1)
wait_ready_sensors()
print("sensors ready")

initial_position = catapult.get_position()

while True:
    try:
        for i in 10: 
            #consistently shoots to the second target
            #TODO: Try to shoot while mounted on the body of the robot 
            catapult.set_position_relative(135)
            time.sleep(1)
            catapult.set_position(initial_position)
            time.sleep(5)
        
        #motor.set_power(40)
        #if TOUCH_SENSOR.is_pressed():
            #print("Touch sensor is pressed")
            
            #Consistently gets into the second one
            #TODO: Increase length of the lever to increase distance 
            #catapult.set_position_relative(155)
            #time.sleep(0.5)
            #catapult.set_position(initial_position)
            
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_position)
        BP.reset_all()
        exit()