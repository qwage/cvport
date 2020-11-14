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

#Motor Power 1-100
power = 40

#Runtime
running = 2

#Rest time
rest = 5

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
        motorAll.forward(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#--------------------------------------------------#

#-----------To Drive the Motors backwards------------# 
        print("Robot Moving Backward ")
        af.off()
        ab.on()
        motorAll.reverse(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#--------------------------------------------------#

#-----------To Drive the Motors Left---------------#
        print("Robot Moving Left ")
        ab.off()
        al.on()
        m1.reverse(power)
        m2.forward(power)
        m3.forward(power)
        m4.reverse(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#--------------------------------------------------#

#----------To Drive the Motors Right---------------#
        print("Robot Moving Right ")
        ar.on()
        al.off()
        m1.forward(power)
        m2.reverse(power)
        m3.reverse(power)
        m4.forward(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#----------To Turn the Motors Right---------------#
        print("Robot Turning Right ")
        m1.forward(power)
        m2.forward(power)
        m3.reverse(power)
        m4.reverse(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#----------To Turn the Motors Left---------------#
        print("Robot Turning Left ")
        m1.reverse(power)
        m2.reverse(power)
        m3.forward(power)
        m4.forward(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#----------To Move 45 Degrees---------------#
        print("Robot Moving 45 Degrees ")
        m1.forward(power)
        m2.stop(power)
        m3.stop(power)
        m4.forward(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#----------To Move 135 Degrees---------------#
        print("Robot Moving 135 Degrees ")
        m1.stop(power)
        m2.forward(power)
        m3.forward(power)
        m4.stop(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#----------To Move 225 Degrees---------------#
        print("Robot Moving 225 Degrees ")
        m1.reverse(power)
        m2.stop(power)
        m3.stop(power)
        m4.reverse(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#----------To Move 315 Degrees---------------#
        print("Robot Moving 315 Degrees ")
        m1.stop(power)
        m2.reverse(power)
        m3.reverse(power)
        m4.stop(power)
        time.sleep(running)
        motorAll.stop()
        time.sleep(rest)
#-------------------------------------------------#

#---------To Stop the Motors----------------------#
        print("Robot Stop ")
        al.off()
        af.off()
        ar.off()
        motorAll.stop()
        time.sleep(running)
#-------------------------------------------------#

        
except KeyboardInterrupt:
    GPIO.cleanup()
