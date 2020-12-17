def disp_out(mess,message,sleep_time,lett,letter,temp,humid,press,comp,gyro,acc):
    
    '''
    #**kargs listing
    key_list = []
    value_list = []
    for key, value in kwargs.items(): 
        key_list.append(key)
        value_list.append(value)
    
    print(key_list)
    '''
    
    from sense_hat import SenseHat
    from time import sleep
    sense = SenseHat()

    #colors for program
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    gray = (128,128,128)
    fuchsia = (255,0,255)
    yellow = (255,255,0)
    aqua = (0,255,255)
    silver = (192,192,192)
    maroon = (128,0,0)
    olive = (128,128,0)
    dark_green =(0,128,0)
    teal = (0,128,128)
    navy = (0,0,128)
    purple = (128,0,128)
    black = (0,0,0)

    if mess == 1:
        #display a message on the screen
        sense.show_message(message, .2, white, black)
        sleep(sleep_time)

    if lett == 1:
        #display only one letter
        sense.show_letter(letter)
        sleep(sleep_time)

    if temp == 1:
        #temperature
        temp = sense.get_temperature()
        print("Temperature: %s C" % temp)

    if humid == 1:
        #humidity
        humidity = sense.get_humidity()
        print("Humidity: %s %%" % humidity)

    if press == 1:
        #pressure
        pressure = sense.get_pressure()
        print("Pressure: %s Millibars" % pressure)

    if comp == 1:
        #compass
        sense.set_imu_config(True, False, False)  # enable only the compass
        north = sense.get_compass()
        print("North: %s" % north)

    if gyro == 1:
        #gyroscope
        sense.set_imu_config(False, True, False)  # gyroscope only
        gyro_only = sense.get_gyroscope()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))
    if acc == 1:
        #accelerometer
        sense.set_imu_config(False, False, True)  # accelerometer only
        accel_only = sense.get_accelerometer()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))

    #turn off the screen
    sense.clear()
