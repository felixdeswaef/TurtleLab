import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

while(1):
 # Spool up motors for 2 seconds
 GPIO.output(23, GPIO.HIGH)
 time.sleep(2)

 # wait 5 seconds
 GPIO.output(23, GPIO.LOW)
 time.sleep(5)
