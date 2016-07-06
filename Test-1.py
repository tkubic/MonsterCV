import RPi.GPIO
import time

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(4, RPi.GPIO.OUT)
RPi.GPIO.setup(17, RPi.GPIO.OUT)

while 1:
    RPi.GPIO.output(4, False) #left
    RPi.GPIO.output(17, True)
    print "on"
    time.sleep(1)
    RPi.GPIO.output(4, False) #off
    RPi.GPIO.output(17, False)
    print "off"
    time.sleep(1)


    
