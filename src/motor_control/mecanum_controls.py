from disp_out import *
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import time
import atexit

power = .5 #Percent of maximum power
delay_time = 5 #Time to run in each direction

mh = Raspi_MotorHAT(addr=0x6f)

#For autodisabling motors at shutdown
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

Motor1 = mh.getMotor(1)
Motor2 = mh.getMotor(2)
Motor3 = mh.getMotor(3)
Motor4 = mh.getMotor(4)

def motor_c(power,delay_time): #Move Forward
    
    speed = int(power*255)

    Motor1.setSpeed(speed)
    Motor1.run(Raspi_MotorHAT.FORWARD)
    Motor2.setSpeed(speed)
    Motor2.run(Raspi_MotorHAT.FORWARD)
    Motor3.setSpeed(speed)
    Motor3.run(Raspi_MotorHAT.FORWARD)
    Motor4.setSpeed(speed)
    Motor4.run(Raspi_MotorHAT.FORWARD)
    disp_out(0,0,delay_time,1,"C",0,0,0,0,0,0)
    turnOffMotors()

def motor_cc(power,delay_time): #Move Backward

    speed = int(power*255)

    Motor1.setSpeed(speed)
    Motor1.run(Raspi_MotorHAT.BACKWARD)
    Motor2.setSpeed(speed)
    Motor2.run(Raspi_MotorHAT.BACKWARD)
    Motor3.setSpeed(speed)
    Motor3.run(Raspi_MotorHAT.BACKWARD)
    Motor4.setSpeed(speed)
    Motor4.run(Raspi_MotorHAT.BACKWARD)
    disp_out(1,"CC",delay_time,0,0,0,0,0,0,0,0)
    turnOffMotors()
    
def motor_b(power,delay_time): #Rotate clockwise

    speed = int(power*255)

    Motor1.setSpeed(speed)
    Motor1.run(Raspi_MotorHAT.FORWARD)
    Motor2.setSpeed(speed)
    Motor2.run(Raspi_MotorHAT.FORWARD)
    Motor3.setSpeed(speed)
    Motor3.run(Raspi_MotorHAT.BACKWARD)
    Motor4.setSpeed(speed)
    Motor4.run(Raspi_MotorHAT.BACKWARD)
    disp_out(0,0,delay_time,1,"B",0,0,0,0,0,0)
    turnOffMotors()
    
def motor_f(power,delay_time): #Rotate counterclockwise

    speed = int(power*255)
    
    Motor1.setSpeed(speed)
    Motor1.run(Raspi_MotorHAT.BACKWARD)
    Motor2.setSpeed(speed)
    Motor2.run(Raspi_MotorHAT.BACKWARD)
    Motor3.setSpeed(speed)
    Motor3.run(Raspi_MotorHAT.FORWARD)
    Motor4.setSpeed(speed)
    Motor4.run(Raspi_MotorHAT.FORWARD)
    disp_out(0,0,delay_time,1,"F",0,0,0,0,0,0)
    turnOffMotors()


