# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO

destroy = 'done'

Timer = 0

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(4, RPi.GPIO.OUT)
RPi.GPIO.setup(17, RPi.GPIO.OUT)
RPi.GPIO.setup(22, RPi.GPIO.OUT)
RPi.GPIO.setup(27, RPi.GPIO.OUT)
p = RPi.GPIO.PWM(22, 50)
m = RPi.GPIO.PWM(27, 50)
p.start(0)
m.start(0)

def Drive(direction):
    # GPIO 27 is 13, GPIO 22 is is 15

    if direction > 0:
        p.ChangeDutyCycle(direction)
        m.ChangeDutyCycle(0)
    elif direction < 0:
        p.ChangeDutyCycle(0)
        m.ChangeDutyCycle(-direction)
    else:
        p.ChangeDutyCycle(0)
        m.ChangeDutyCycle(0)

def Turn(speed):
    #port 2 is 5v, 6 is ground, GPIO 4 is 7, GPIO 17 is is 11
    
    if speed == 1:
        RPi.GPIO.output(4, True) #right
        RPi.GPIO.output(17, False)
    elif speed == 0 or speed == 2:
        RPi.GPIO.output(4, False) #straight
        RPi.GPIO.output(17, False)
    else:
        RPi.GPIO.output(4, False) #left
        RPi.GPIO.output(17, True)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# define range of blue color in HSV
lower_blue = np.array([52, 0, 240])
upper_blue = np.array([60, 10, 255])

# Resize Window
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

direction = 2
first = 1
while 1:
    rawCapture = PiRGBArray(camera)
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only white
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    imgContours, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    if contours:
        (x, y), radius = cv2.minEnclosingCircle(contours[0])
        center = (int(x), int(y))
        radius = int(radius)
    else:
        radius = -1
        
    #0 means lost, 1 meals right, -1 means left, 2 means straight
    if radius == -1:
        direction = 0
    elif x >= 370:
        direction = 1
    elif x <= 270:
        direction = -1
    else:
        direction = 2
    Turn(direction)

    #speed is percent out of 100
    if radius > 200:
        speed = 0
    elif radius > 0:
        speed = 75
    else:
        speed = 0

    #speed is percent out of 100
    Drive(speed)

    print direction
    
    # display the image on screen and wait for a keypress
    cv2.imshow("Image", mask)
    cv2.waitKey(1)

    first = 0
    
cv2.destroyAllWindows()
p.stop()
m.stop()
GPIO.cleanup()



