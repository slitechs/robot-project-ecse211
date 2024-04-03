from utils.brick import Motor, TouchSensor, wait_ready_sensors, BP  
import time

#motor = Motor("A")
door = Motor("A")

#wait_ready_sensors()
#print("sensors ready")

initial_position = door.get_position() #get initial position
print("Initial Position: " + str(initial_position))

i = 1 #Counter (1 to 10)

while True:
    try:
        time.sleep(1)
        door.set_position_relative(-45) 
        print("Open: " + str(i))
        time.sleep(0.45) #0.35
        door.set_position(initial_position)
        print("Close: " + str(i))
        time.sleep(2)
        i +=1
            
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        #motor.set_power(0)
        door.set_position(initial_position)
        BP.reset_all()
        exit()
        

        
