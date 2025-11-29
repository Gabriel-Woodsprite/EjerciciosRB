import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
  if GPIO.input(27) == GPIO.LOW:
    print("Botòn Presionado")