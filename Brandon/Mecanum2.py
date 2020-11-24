#!/usr/bin/python
import math
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

def set_speeds(angle):
    #Set the speed of each motor with -1 being max reverse and 1 being max forward
    #s1 is the speed of the top left motor, s2 is the bottom left, s3 is the top right, s4 is the bottom right
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    angle = angle*math.pi/180
    if angle >= 0 and angle <= math.pi/2:
        #Between 0 and pi/2 motors 1 and 4 should be at full power forward and 2 and 3 will vary
        s1 = 1
        s4 = 1
        s2 = -math.cos(2*angle)
        s3 = -math.cos(2*angle)
    elif angle >= -math.pi and angle <= -math.pi/2:
        #Between -pi and -pi/2 motors 1 and 4 will be at full power reverse and 2 and 3 will vary 
        s1 = -1
        s4 = -1
        s2 = math.cos(2*angle)
        s3 = math.cos(2*angle)
    elif angle >= -math.pi/2 and angle <= 0:
        #Between 0 and -pi/2 motors 2 and 3 will be at full power reverse while 1 and 4 will vary 
        s1 = math.cos(2*angle)
        s4 = math.cos(2*angle)
        s2 = -1
        s3 = -1
    else:
        #Between pi/2 and pi motors 2 and 3 will be at full power forward while 1 and 4 will vary
        s1 = -math.cos(2*angle)
        s4 = -math.cos(2*angle)
        s2 = 1
        s3 = 1
    #Scale speeds to pass to motors
    s1 *= 255
    s2 *= 255
    s3 *= 255
    s4 *= 255
    return(s1,s2,s3,s4)

def turn_motor(speed,motor):
    #Sets the motor speed and direction
    #Positive speed inputs will result in forward motion while negative speed inputs will result in reverse
    if speed >= 0:
        motor.setSpeed(speed)
        motor.run(Raspi_MotorHAT.FORWARD)
    elif speed <= 0:
        speed *= -1
        motor.setSpeed(speed)
        motor.run(Raspi_MotorHAT.BACKWARD)
    return

def rotate_clockwise(power):
    #Turns vehicle clockwise
    speed = power * 255
    Motor1.setSpeed(speed)
    Motor1.run(Raspi_MotorHAT.FORWARD)
    Motor2.setSpeed(speed)
    Motor2.run(Raspi_MotorHAT.FORWARD)
    Motor3.setSpeed(speed)
    Motor3.run(Raspi_MotorHAT.BACKWARD)
    Motor4.setSpeed(speed)
    Motor4.run(Raspi_MotorHAT.BACKWARD)
    return

def rotate_counterclockwise(power):
    #Turns vehicle counterclockwise
    speed = power * 255
    Motor1.setSpeed(speed)
    Motor1.run(Raspi_MotorHAT.BACKWARD)
    Motor2.setSpeed(speed)
    Motor2.run(Raspi_MotorHAT.BACKWARD)
    Motor3.setSpeed(speed)
    Motor3.run(Raspi_MotorHAT.FORWARD)
    Motor4.setSpeed(speed)
    Motor4.run(Raspi_MotorHAT.FORWARD)
    return

