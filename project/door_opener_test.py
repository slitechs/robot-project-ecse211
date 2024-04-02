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
        door.set_position_relative(-45) #115 for 3rd,65 for 2nd, 50 for 1st
        print("Open: " + str(i))
        time.sleep(0.3) #0.35
        door.set_position(initial_position)
        print("Close: " + str(i))
        time.sleep(2)
        i +=1
        
        #door.set_power(-35)
        #time.sleep(0.2)
        #door.set_power(35)
        #time.sleep(0.21)
        #door.set_power(0)
        #time.sleep(4)
        
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
        door.set_position(initial_position)
        BP.reset_all()
        exit()
        

        
