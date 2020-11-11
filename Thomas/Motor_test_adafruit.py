#Each direction should run for 1 second then coast for 3 before
#fulling stopping, hopefully this prevents breaking the motor hat

#For the none variable for coasting it should be coming from the adafruit files

import time
import board
from adafruit_motorkit import MotorKit
kit = MotorKit()

#For this test we will use 40% power
power = .4

#Unit is seconds
runnning = 1   #How long the motors run for each test
coasting = 3   #How long the motors coast for each test
stopped = 1.5  #Pause between stopping motors and starting next test
#These set the power for each motor
m1_power = kit.motor1.throttle
m2_power = kit.motor2.throttle
m3_power = kit.motor3.throttle
m4_power = kit.motor4.throttle

#Forward
m1_power = power
m2_power = power
m3_power = power
m4_power = power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#Reverse
m1_power = -power
m2_power = -power
m3_power = -power
m4_power = -power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#Left
m1_power = -power
m2_power = power
m3_power = power
m4_power = -power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#Right
m1_power = power
m2_power = -power
m3_power = -power
m4_power = power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#Clockwise Rotation
m1_power = power
m2_power = power
m3_power = -power
m4_power = -power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped1)

#Counter-Clockwise Rotation
m1_power = -power
m2_power = -power
m3_power = power
m4_power = power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#45 Degree movement
m1_power = power
m4_power = power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#135 Degree movement
m2_power = power
m3_power = power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#225 Degree movement
m1_power = -power
m4_power = -power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)

#315 Degree movement
m2_power = -power
m3_power = -power

time.sleep(runnning)

m1_power = none
m2_power = none
m3_power = none
m4_power = none

time.sleep(coasting)

m1_power = 0
m2_power = 0
m3_power = 0
m4_power = 0

time.sleep(stopped)