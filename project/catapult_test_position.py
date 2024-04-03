from utils.brick import Motor, TouchSensor, wait_ready_sensors, BP  
import time

#motor = Motor("A")
catapult = Motor("B")
door = Motor("A")
TOUCH_SENSOR = TouchSensor(1)
wait_ready_sensors()
print("sensors ready")

initial_position = catapult.get_position()
print(initial_position)

while True:
    try:
        for i in range(8):
            time.sleep(1)
            catapult.set_position_relative(125) #125 for 3rd, 65 for 2nd, 50 for 1st
            time.sleep(1.0)
            catapult.set_position(initial_position)
            time.sleep(4)
            
        time.sleep(1)
        catapult.set_position_relative(65) 
        time.sleep(1.0)
        catapult.set_position(initial_position)
        time.sleep(2)
        
        time.sleep(1)
        catapult.set_position_relative(50) 
        time.sleep(1.0)
        catapult.set_position(initial_position)
        time.sleep(2)
        break
        #motor.set_power(40)
        #if TOUCH_SENSOR.is_pressed():
            #print("Touch sensor is pressed")
           
    
            
            #Consistently gets into the second one
            #TODO: Increase length of the lever to increase distance
            #With increased length of lever, angle > 150 hits the table
            #catapult.set_position_relative(158)
        
            #catapult.set_position_relative(150)
            #catapult.set_position_relative(145)
       
            
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_position)
        BP.reset_all()
        exit()
        

        