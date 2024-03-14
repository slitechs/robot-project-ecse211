from utils.brick import BP, Motor, wait_ready_sensors, EV3ColorSensor, TouchSensor

print("Program start.\nWaiting for sensors to turn on...")
motorRight = Motor("C")
motorLeft = Motor("D")

colorRight = EV3ColorSensor(4)
colorLeft = EV3ColorSensor(3)

touch_sensor = TouchSensor(1)
wait_ready_sensors()
print("Done waiting")

#TODO: Implement the color sensor in navigation so it keeps going straight 
while True:
    try:
        #print(GYRO_SENSOR.get_abs_measure())
        if touch_sensor.is_pressed():
            motorLeft.set_power(-50)
            motorRight.set_power(-50)

    except BaseException:
        motorLeft.set_power(0)
        motorRight.set_power(0)
        exit()