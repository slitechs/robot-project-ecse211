from utils.brick import Motor, TouchSensor, wait_ready_sensors, BP  
import time

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
       
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        catapult.set_position(initial_position)
        BP.reset_all()
        exit()
        

        