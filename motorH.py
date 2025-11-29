import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
IN1, IN2 = 5,6

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

GPIO.output(IN1, True)
GPIO.output(IN2, False)
time.sleep(3)
GPIO.output(IN1, False)
GPIO.output(IN2, True)