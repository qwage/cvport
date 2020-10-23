# Osoyoo Model-Pi L298N DC motor driver programming guide
# tutorial url: https://osoyoo.com/2020/03/01/python-programming-tutorial-model-pi-l298n-motor-driver-for-raspberry-pi/

import RPi.GPIO as GPIO #control motor board through GPIO pins
import time #set delay time to control moving distance

#If IN1Rear=True and IN2Rear=False right motor move forward, If IN1Rear=False,IN2Rear=True right motor move backward,in other cases right motor stop
IN1Rear = 16 #GPIO23 to IN1 Rear-right wheel direction 
IN2Rear = 18 #GPIO24 to IN2 Rear-right wheel direction

#If IN3Rear=True and IN3Rear=False left motor move forward, If IN3Rear=False,IN4Rear=True left motor move backward,in other cases left motor stop
IN3Rear = 13 #GPIO27 to IN3 Rear-left wheel direction
IN4Rear = 15 #GPIO22 to IN4 Rear-left wheel direction

#ENA/ENB are PWM(analog) signal pin which control the speed of right/left motor through GPIO ChangeDutyCycle(speed) function
ENA = 12 #GPIO18 to ENA PWM SPEED of rear left motor
ENB = 33 #GPIO13 to ENB PWM SPEED of rear right motor

#If IN1Front=True and IN2Front=False right motor move forward, If IN1Front=False,IN2Front=True right motor move backward,in other cases right motor stop
IN1Front = 40 #GPIO21 to IN1 Front Model X right wheel direction 
IN2Front = 38 #GPIO20 to IN2 Front Model X right wheel direction

#If IN3Front=True and IN3Front=False left motor move forward, If IN3Front=False,IN4Front=True left motor move backward,in other cases left motor stop
IN3Front = 36 #GPIO16 to IN3 Front Model X left wheel direction
IN4Front = 32 #GPIO12 to IN4 Front Model X left wheel direction

#initialize GPIO pins, tell OS which pins will be used to control Model-Pi L298N board
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1Rear, GPIO.OUT) 
GPIO.setup(IN2Rear, GPIO.OUT)
GPIO.setup(IN3Rear, GPIO.OUT)
GPIO.setup(IN4Rear, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN1Front, GPIO.OUT) 
GPIO.setup(IN2Front, GPIO.OUT)
GPIO.setup(IN3Front, GPIO.OUT)
GPIO.setup(IN4Front, GPIO.OUT)
GPIO.output(ENA,True)
GPIO.output(ENB,True)

#following code only works when using Model-Pi instead of Model X motor driver board which can give raspberry Pi USB 5V power
#Initialize Rear model X board ENA and ENB pins, tell OS that ENA,ENB will output analog PWM signal with 1000 frequency
#rightSpeed = GPIO.PWM(ENA,1000)	
#leftSpeed = GPIO.PWM(ENB,1000)	
#rightSpeed.start(0)
#leftSpeed.start(0)

#make rear right motor moving forward
def rr_ahead(speed):
    GPIO.output(IN1Rear,True)
    GPIO.output(IN2Rear,False)

    #ChangeDutyCycle(speed) function can change the motor rotation speed
    #rightSpeed.ChangeDutyCycle(speed)

#make rear left motor moving forward    
def rl_ahead(speed):  
    GPIO.output(IN3Rear,True)
    GPIO.output(IN4Rear,False)
    #leftSpeed.ChangeDutyCycle(speed)
    
#make rear right motor moving backward
def rr_back(speed):
    GPIO.output(IN2Rear,True)
    GPIO.output(IN1Rear,False)

    #ChangeDutyCycle(speed) function can change the motor rotation speed
    #rightSpeed.ChangeDutyCycle(speed)

#make rear left motor moving backward    
def rl_back(speed):  
    GPIO.output(IN4Rear,True)
    GPIO.output(IN3Rear,False)
    #leftSpeed.ChangeDutyCycle(speed)
    
    
#make front right motor moving forward
def fr_ahead(speed):
    GPIO.output(IN1Front,True)
    GPIO.output(IN2Front,False)

#make Front left motor moving forward    
def fl_ahead(speed):  
    GPIO.output(IN3Front,True)
    GPIO.output(IN4Front,False)
 
    
#make Front right motor moving backward
def fr_back(speed):
    GPIO.output(IN2Front,True)
    GPIO.output(IN1Front,False)

#make Front left motor moving backward    
def fl_back(speed):  
    GPIO.output(IN4Front,True)
    GPIO.output(IN3Front,False)

    
def go_ahead(speed):
    rl_ahead(speed)
    rr_ahead(speed)
    fl_ahead(speed)
    fr_ahead(speed)
    
def go_back(speed):
    rr_back(speed)
    rl_back(speed)
    fr_back(speed)
    fl_back(speed)

#making right turn   
def turn_right(speed):
    rl_ahead(speed)
    rr_back(speed)
    fl_ahead(speed)
    fr_back(speed)
      
#make left turn
def turn_left(speed):
    rr_ahead(speed)
    rl_back(speed)
    fr_ahead(speed)
    fl_back(speed)

# parallel left shift 
def shift_left(speed):
    fr_ahead(speed)
    rr_back(speed)
    rl_ahead(speed)
    fl_back(speed)

# parallel right shift 
def shift_right(speed):
    fr_back(speed)
    rr_ahead(speed)
    rl_back(speed)
    fl_ahead(speed)

def upper_right(speed):
    rr_ahead(speed)
    fl_ahead(speed)

def lower_left(speed):
    rr_back(speed)
    fl_back(speed)
    
def upper_left(speed):
    fr_ahead(speed)
    rl_ahead(speed)

def lower_right(speed):
    fr_back(speed)
    rl_back(speed)

#make both motor stop
def stop_car():
    GPIO.output(IN1Rear,False)
    GPIO.output(IN2Rear,False)
    GPIO.output(IN3Rear,False)
    GPIO.output(IN4Rear,False)
    GPIO.output(IN1Front,False)
    GPIO.output(IN2Front,False)
    GPIO.output(IN3Front,False)
    GPIO.output(IN4Front,False)
    #leftSpeed.ChangeDutyCycle(0)
    #rightSpeed.ChangeDutyCycle(0)

go_ahead(100)
time.sleep(1)
stop_car()

go_back(100)
time.sleep(1)
stop_car()

turn_left(100)
time.sleep(1)
stop_car()

turn_right(100)
time.sleep(1)
stop_car()

shift_right(100)
time.sleep(1)
stop_car()

shift_left(100)
time.sleep(1)
stop_car()

upper_left(100)
time.sleep(1)
stop_car()

lower_right(100)
time.sleep(1)
stop_car()

upper_right(100)
time.sleep(1)
stop_car()

lower_left(100)
time.sleep(1)
stop_car()

GPIO.cleanup()    