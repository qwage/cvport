#!/usr/bin/python

import PiMotor
import time
import RPi.GPIO as GPIO

#Name of Individual MOTORS 
m1 = PiMotor.Motor("MOTOR1",1)  #Front Left
m2 = PiMotor.Motor("MOTOR2",1)  #Rear Left
m3 = PiMotor.Motor("MOTOR3",1)  #Front Right 
m4 = PiMotor.Motor("MOTOR4",1)  #Rear Right

#To drive all motors together
motorAll = PiMotor.LinkedMotors(m1,m2,m3,m4)

#Names for Individual Arrows
ab = PiMotor.Arrow(1)
al = PiMotor.Arrow(2)
af = PiMotor.Arrow(3) 
ar = PiMotor.Arrow(4)

##This segment drives the motors in the direction listed below:
## forward and reverse takes speed in percentage(0-100)

try:
    while True:
#-----------To Drive the Motors Forward------------# 
        print("Robot Moving Forward ")
        af.on()
        motorAll.forward(100)
        time.sleep(5)
#--------------------------------------------------#

#-----------To Drive the Motors backwards------------# 
        print("Robot Moving Backward ")
        af.off()
        ab.on()
        motorAll.reverse(100)
        time.sleep(5)
#--------------------------------------------------#

#-----------To Drive the Motors Left---------------#
        print("Robot Moving Left ")
        ab.off()
        al.on()
        m1.reverse(100)
        m2.forward(100)
        m3.forward(100)
        m4.reverse(100)
        time.sleep(5)
#--------------------------------------------------#

#----------To Drive the Motors Right---------------#
        print("Robot Moving Right ")
        ar.on()
        al.off()
        m1.forward(100)
        m2.reverse(100)
        m3.reverse(100)
        m4.forward(100)
        time.sleep(5)
#-------------------------------------------------#

#----------To Turn the Motors Right---------------#
        print("Robot Turning Right ")
        m1.forward(100)
        m2.forward(100)
        m3.reverse(100)
        m4.reverse(100)
        time.sleep(5)
#-------------------------------------------------#

#----------To Turn the Motors Left---------------#
        print("Robot Turning Left ")
        m1.reverse(100)
        m2.reverse(100)
        m3.forward(100)
        m4.forward(100)
        time.sleep(5)
#-------------------------------------------------#

#----------To Move 45 Degrees---------------#
        print("Robot Moving 45 Degrees ")
        m1.forward(100)
        m2.stop(100)
        m3.stop(100)
        m4.forward(100)
        time.sleep(5)
#-------------------------------------------------#

#----------To Move 135 Degrees---------------#
        print("Robot Moving 135 Degrees ")
        m1.stop(100)
        m2.forward(100)
        m3.forward(100)
        m4.stop(100)
        time.sleep(5)
#-------------------------------------------------#

#----------To Move 225 Degrees---------------#
        print("Robot Moving 225 Degrees ")
        m1.reverse(100)
        m2.stop(100)
        m3.stop(100)
        m4.reverse(100)
        time.sleep(5)
#-------------------------------------------------#

#----------To Move 315 Degrees---------------#
        print("Robot Moving 315 Degrees ")
        m1.stop(100)
        m2.reverse(100)
        m3.reverse(100)
        m4.stop(100)
        time.sleep(5)
#-------------------------------------------------#

#---------To Stop the Motors----------------------#
        print("Robot Stop ")
        al.off()
        af.off()
        ar.off()
        motorAll.stop()
        time.sleep(5)
#-------------------------------------------------#

        
except KeyboardInterrupt:
    GPIO.cleanup()
