from utils.brick import Motor, wait_ready_sensors, BP  
import time
import threading

catapult = Motor("B")
door = Motor("A") 
wait_ready_sensors()
print("Ready")

initial_door_position = door.get_position() #get initial position
print(initial_door_position)
initial_catapult_position = catapult.get_position()
print(initial_catapult_position)

def third_bucket():
    try: 
        for i in range(8): 
            time.sleep(1)
            door.set_position_relative(-45)
            print("open door")
            time.sleep(0.40)
            door.set_position(initial_door_position)
            print("close door")
            time.sleep(1)
            catapult.set_position_relative(125) #125 for 3rd,65 for 2nd, 55 for 1st
            time.sleep(1.0)
            catapult.set_position(initial_catapult_position)
            time.sleep(1) 

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_catapult_position)
        door.set_position(initial_door_position)
        BP.reset_all()
        exit()

def second_bucket():
    try:
        time.sleep(1)
        door.set_position_relative(-45)
        print("open door")
        time.sleep(0.40)
        door.set_position(initial_door_position)
        print("close door")
        time.sleep(1)
        catapult.set_position_relative(65) 
        time.sleep(1.0)
        catapult.set_position(initial_catapult_position)
        time.sleep(1) 

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_catapult_position)
        door.set_position(initial_door_position)
        BP.reset_all()
        exit()
        
def first_bucket():
    try:
        time.sleep(1)
        door.set_position_relative(-45)
        print("open door")
        time.sleep(0.40)
        door.set_position(initial_door_position)
        print("close door")
        time.sleep(1)
        catapult.set_position_relative(50) 
        time.sleep(1.0)
        catapult.set_position(initial_catapult_position)
        time.sleep(1) 

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_catapult_position)
        door.set_position(initial_door_position)
        BP.reset_all()
        exit()

if __name__ == "__main__": 
    first_bucket()
    second_bucket()
    third_bucket()

    
