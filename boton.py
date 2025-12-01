import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)

i = 0
while True:
  if GPIO.input(27) != GPIO.HIGH:
    print(f'{i} Botòn Presionado')
    i = i+1