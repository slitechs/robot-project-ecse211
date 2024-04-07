from utils.brick import Motor, TouchSensor, wait_ready_sensors, BP  
import time

catapult = Motor("B")

def signalf(): 
    try: 
        initial_position = catapult.get_position()
        time.sleep(1.0)
        catapult.set_position_relative(30) 
        time.sleep(1.0)
        catapult.set_position(initial_position)
    
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print("stop signal")
        catapult.set_position(initial_position)
        BP.reset_all()
        exit() 



