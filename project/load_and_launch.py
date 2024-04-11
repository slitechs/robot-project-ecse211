from utils.brick import Motor, wait_ready_sensors, BP  
import time
import threading

#Battery 31 (maybe?): 90 for 3rd,69 for 2nd, 53 for 1st
#Battery 32: 

catapult = Motor("B")
door = Motor("A")
motorRight = Motor("C")
motorLeft = Motor("D")
wait_ready_sensors()
print("Ready")

initial_door_position = door.get_position() #get initial position
print(initial_door_position)
initial_catapult_position = catapult.get_position()
print(initial_catapult_position)

def third_bucket():
    try:
        """for i in range(3): 
            for i in range(2): 
                time.sleep(1)
                door.set_position_relative(-60)
                time.sleep(0.65)
                door.set_position(initial_door_position)
                time.sleep(1)
                catapult.set_position_relative(90) #90 for 3rd,65 for 2nd, 50 for 1st
                time.sleep(1.0)
                catapult.set_position(initial_catapult_position)
                time.sleep(1)
            motorRight.set_power(-10)
            motorLeft.set_power(10)
            time.sleep(0.2)
            motorRight.set_power(0)
            motorLeft.set_power(0)
            
        for i in range(2):
            time.sleep(1)
            door.set_position_relative(-60)
            time.sleep(0.65)
            door.set_position(initial_door_position)
            time.sleep(1)
            catapult.set_position_relative(90) #90 for 3rd,65 for 2nd, 50 for 1st
            time.sleep(1.0)
            catapult.set_position(initial_catapult_position)
            time.sleep(1)
            motorRight.set_power(-10)
            motorLeft.set_power(10)
            time.sleep(0.25)
            motorRight.set_power(0)
            motorLeft.set_power(0)"""
        for i in range(10):
            time.sleep(1)
            door.set_position_relative(-60)
            time.sleep(0.65)
            door.set_position(initial_door_position)
            time.sleep(1)
            catapult.set_position_relative(94) 
            time.sleep(1.0)
            catapult.set_position(initial_catapult_position)
            time.sleep(1)
            motorRight.set_power(-10)
            motorLeft.set_power(10)
            time.sleep(0.12)
            motorRight.set_power(0)
            motorLeft.set_power(0)

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        catapult.set_position(initial_catapult_position)
        door.set_position(initial_door_position)
        BP.reset_all()
        exit()

def second_bucket():
    try:
        time.sleep(1)
        door.set_position_relative(-55)
        time.sleep(0.65)
        door.set_position(initial_door_position)
        time.sleep(1)
        catapult.set_position_relative(75)  # was 70 but too little
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
        door.set_position_relative(-55)
        time.sleep(0.65)
        door.set_position(initial_door_position)
        time.sleep(1)
        catapult.set_position_relative(60) # was 55 but too little
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

    
