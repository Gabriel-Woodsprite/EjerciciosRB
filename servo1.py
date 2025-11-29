import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18,50)
pwm.start(0)

def mover(angulo):
  duty = 2+(angulo/18)
  pwm.ChangeDutyCycle(duty)
  time.sleep(0.5)
  
mover(0);
mover(90);
mover(180)

pwm.stop()
GPIO.cleanup()