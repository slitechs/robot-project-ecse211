from utils.brick import Motor, wait_ready_sensors, BP  
import time
import threading

catapult = Motor("B")
door = Motor("A") 
wait_ready_sensors()
print("Ready")

initial_door_position = door.get_position() #get initial position
initial_catapult_position = catapult.get_position()

def door_open():
    try:
        for i in range(10):
            time.sleep(1)
            door.set_position_relative(-45) 
            time.sleep(0.40)
            door.set_position(initial_door_position)
            time.sleep(2)
        
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        door.set_position(initial_door_position)
        BP.reset_all()
        exit()
        
def catapult_launch():
    try:
        for i in range(1, 11):
            if (i <= 8): 
                time.sleep(1)
                catapult.set_position_relative(125) #125 for 3rd,80 for 2nd, 55 for 1st
                time.sleep(1.0)
                catapult.set_position(initial_catapult_position)
                time.sleep(2)
            
            elif (i == 9):
                time.sleep(1)
                catapult.set_position_relative(80) 
                time.sleep(1.0)
                catapult.set_position(initial_catapult_position)
                time.sleep(2)
            else: 
                time.sleep(1)
                catapult.set_position_relative(55) 
                time.sleep(1.0)
                catapult.set_position(initial_catapult_position)
                time.sleep(2)

            i += 1

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_catapult_position)
        BP.reset_all()
        exit()

def load_and_launch(): 
    try: 
        # Initialize threads for both functions
        door_thread = threading.Thread(target=door_open)
        catapult_thread = threading.Thread(target=catapult_launch)

        # Start threads
        door_thread.start()
        catapult_thread.start()

        # Optionally, wait for both threads to complete
        door_thread.join()
        catapult_thread.join()
    
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        BP.reset_all()
        exit()

if __name__ == "__main__": 
    load_and_launch()