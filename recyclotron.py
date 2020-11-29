import RPi.GPIO as GPIO
# import test
import time
#from picamera import PiCam

#import torch-raspi
import random

#camera = PiCamera()
MOTOR_PWM = 17
MOTOR_DIRECTION = 27
LIMIT = 18
FORCE = 26
RELAYa = 21 # check if these two are correct
RELAYb = 20
SERVO = 23
CPR = 64
x = 12.5
y = 15.3
FLAT_PWM = 6
MOTORa = 20
MOTORb = 21



# GPIO.input(LIMIT) == 1 when not pressed and 0 when pressed
def limit():
    print(GPIO.input(LIMIT))
    return (GPIO.input(LIMIT) == 0)

#180 degrees : 73
#45 degrees : 18
#135 degrees : 44
# 225 : 61
# 315 :

def motor(angle):                                                                    
    # pick appropriate ports for RELAYa, RELAYb
    print("powering the motor")
    if angle == -1:                                   
        #go back until limit switch cries
        while(not limit()):
            #reverse
            GPIO.output(MOTOR_DIRECTION, GPIO.HIGH)
            GPIO.output(MOTOR_PWM, GPIO.LOW)
        GPIO.output(MOTOR_DIRECTION, GPIO.LOW)
        GPIO.output(MOTOR_DIRECTION, GPIO.LOW)
    else:
        #go forward by angle
        cnt = 0
        GPIO.output(MOTOR_DIRECTION, GPIO.HIGH)
        GPIO.output(MOTOR_PWM, GPIO.HIGH)
        
        lma = 0
        lmb = 0
        while cnt < angle*CPR/360:
            # pick appropriate ports for MOTORa, MOTORb
            GPIO.output(MOTOR_DIRECTION, GPIO.HIGH)
            GPIO.output(MOTOR_PWM, GPIO.HIGH)
            #print(ma)
            #print(mb)
            # if (lma != ma) or (lmb != mb):
            cnt += 1
            #lma = ma
           # lmb = mb
            print(cnt)
        GPIO.output(MOTOR_DIRECTION, GPIO.LOW)
        GPIO.output(MOTOR_PWM, GPIO.LOW)

# 1s - 45 degrees
# 2.5s - 135 degrees
# 4.25s - 225 degrees
# 6s - 315 degrees

def rotate(t):
    if(t == -1):
        #relax()
        GPIO.output(MOTOR_DIRECTION, GPIO.HIGH)
        GPIO.output(MOTOR_PWM, GPIO.HIGH)
        pwm.start(50)
        while(not limit()):
            #pwm.start(0)
            #time.sleep(0.25)
            pwm.start(20)
            time.sleep(0.1)
        pwm.start(0)
    else:
        print("lol")
        GPIO.output(MOTOR_DIRECTION, GPIO.LOW)
        GPIO.output(MOTOR_PWM, GPIO.HIGH)
        pwm.start(25)
        time.sleep(t)
        pwm.start(0)


    #pwm.ChangeDutyCycle(50)
    
    #GPIO.output(RELAYa, GPIO.HIGH)
    
def detect_weight() :
    #4.5% to 20.5% 
    #hold()
    vol = GPIO.input(FORCE)
    print(vol)
    if(vol == 1):
        return True
    return False
    
def drop():

    #4.5% to 20.5% 
    pwm_servo.start(12.5)
    time.sleep(2)
    pwm_servo.ChangeDutyCycle(FLAT_PWM)
    # for i in range (1,27):
      #  pwm.ChangeDutyCycle(val)
       # print("Hello")
    #pwm.ChangeDutyCycle(5)

    time.sleep(1)
    print("haha")
    
    
def take_photo():
    print("takes photo and calls classify function")
    #camera.capture('/home/pi/Desktop/image.jpg')
# def classify():
  #  print("takes photo and calls classify function")
   # camera.capture('/home/pi/Desktop/image.jpg')
    #result = test.classify()
    #if result == 'cans':
     #   motor(45)
    #elif result == 'carton':
     #   motor(135)
    #elif result == 'kz':
       # motor(225)
    #else:
     #   motor(315)
    #drop()
    #motor(-1)
     
def hold():
    pwm_servo.start(FLAT_PWM)

def relax():
    pwm_servo.stop()
    
def idle():
    print("idle function, waits for force...")
    while 1:
        if GPIO.input(FORCE):
            classify()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTORa, GPIO.IN)
GPIO.setup(MOTORb, GPIO.IN)
GPIO.setup(LIMIT, GPIO.IN)
GPIO.setup(FORCE, GPIO.IN)
GPIO.setup(MOTOR_DIRECTION, GPIO.OUT)
GPIO.setup(MOTOR_PWM, GPIO.OUT)
GPIO.setup(SERVO, GPIO.OUT)
pwm = GPIO.PWM(MOTOR_PWM, 100)
pwm_servo = GPIO.PWM(SERVO, 50)

'''
hold()
while(True):
    if(detect_weight()):
        time.sleep(2)
        take_photo()
        break
'''
    
x=0
rotate(0.4)
while(True):
    hold()
    #if(detect_weight()):
        #take_photo()
        #classity()
        #x = random.randint(0, 4)
    #time.sleep(3)
    x=x+1
    if x == 0:
        rotate(0.4)
    elif x == 1:
        rotate(1)
    elif x == 2:
        rotate(1.8)
    else:
        rotate(2.6)
        #relax()
    time.sleep(1)
    drop()
    rotate(-1)
      
    

    
        #rotate(-1)
#motor(1000)
#while(1):
#    detect_weight()
#drop(1)
#while (limit()):
#detect_weight()
#if(detect_weight()):
     # identify
    #angle = 44
    #motor(angle)
#drop()
        #motor(-1)
      
#drop(x)
#motor(100)
