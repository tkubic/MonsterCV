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

print "start"

RPi.GPIO.output(4, True)
RPi.GPIO.output(17, True)
RPi.GPIO.output(22, True)
RPi.GPIO.output(27, True)

time.sleep(10)

RPi.GPIO.output(4, False)
RPi.GPIO.output(17, False)
RPi.GPIO.output(22, False)
RPi.GPIO.output(27, False)

print "done"
