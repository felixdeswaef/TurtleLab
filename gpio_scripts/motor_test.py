import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

while(1):
<<<<<<< HEAD:ws2812b/gpio_test.py
 GPIO.output(25, GPIO.HIGH)
 time.sleep(1)
 GPIO.output(25, GPIO.LOW)
 time.sleep(1)
=======
 # Spool up motors for 2 seconds
 GPIO.output(23, GPIO.HIGH)
 time.sleep(2)

 # wait 5 seconds
 GPIO.output(23, GPIO.LOW)
 time.sleep(5)
>>>>>>> c11b8417d6ba10f061f396df0f457d581c188c48:gpio_scripts/motor_test.py
