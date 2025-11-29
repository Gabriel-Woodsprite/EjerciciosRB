import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4

while True:
  h, t = Adafruit_DHT.read(sensor, pin)
  print(f'Temperatura: {t} | Humedad: {h}')