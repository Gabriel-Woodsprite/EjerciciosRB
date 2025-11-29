import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
leds = [17,22,24]
for pin in leds:
  GPIO.setup(pin, GPIO.OUT)
  
while True:
  GPIO.output(17, True); time.sleep(2)
  GPIO.output(17, False)
  GPIO.output(22, True); time.sleep(1)
  GPIO.output(22, False)
  GPIO.output(24, True); time.sleep(2)
  GPIO.output(24, False)
  