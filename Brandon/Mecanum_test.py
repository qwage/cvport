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

speed = int(power*255)
#Move forward
Motor1.setSpeed(speed)
Motor1.run(Raspi_MotorHAT.FORWARD)
Motor2.setSpeed(speed)
Motor2.run(Raspi_MotorHAT.FORWARD)
Motor3.setSpeed(speed)
Motor3.run(Raspi_MotorHAT.FORWARD)
Motor4.setSpeed(speed)
Motor4.run(Raspi_MotorHAT.FORWARD)
time.sleep(delay_time)

turnOffMotors()
time.sleep(delay_time/2)

#Move backward
Motor1.setSpeed(speed)
Motor1.run(Raspi_MotorHAT.BACKWARD)
Motor2.setSpeed(speed)
Motor2.run(Raspi_MotorHAT.BACKWARD)
Motor3.setSpeed(speed)
Motor3.run(Raspi_MotorHAT.BACKWARD)
Motor4.setSpeed(speed)
Motor4.run(Raspi_MotorHAT.BACKWARD)
time.sleep(delay_time)

turnOffMotors()
time.sleep(delay_time/2)

#Rotate clockwise
Motor1.setSpeed(speed)
Motor1.run(Raspi_MotorHAT.FORWARD)
Motor2.setSpeed(speed)
Motor2.run(Raspi_MotorHAT.FORWARD)
Motor3.setSpeed(speed)
Motor3.run(Raspi_MotorHAT.BACKWARD)
Motor4.setSpeed(speed)
Motor4.run(Raspi_MotorHAT.BACKWARD)
time.sleep(delay_time)

turnOffMotors()
time.sleep(delay_time/2)

#Rotate counterclockwise
Motor1.setSpeed(speed)
Motor1.run(Raspi_MotorHAT.BACKWARD)
Motor2.setSpeed(speed)
Motor2.run(Raspi_MotorHAT.BACKWARD)
Motor3.setSpeed(speed)
Motor3.run(Raspi_MotorHAT.FORWARD)
Motor4.setSpeed(speed)
Motor4.run(Raspi_MotorHAT.FORWARD)
time.sleep(delay_time)

turnOffMotors()


