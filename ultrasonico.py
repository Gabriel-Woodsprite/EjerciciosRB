import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

while True:
  GPIO.output(TRIG,True)
  time.sleep(0.00001)
  GPIO.output(TRIG,False)
  
  while GPIO.input(ECHO) == 0:
    inicio = time.time()
    
  while GPIO.input(ECHO)==1:
    fin = time.time();
    
  distancia = (fin-inicio)*17000
  print(f'Distancia: {distancia}cm')
  time.sleep(3)