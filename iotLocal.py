import AdaFruit_DHT
import request, time

while True:
  h,t = AdaFruit_DHT.read(AdaFruit_DHT.DHT11,4)
  datos = {"Temp": t, "Hum": 4}
  print(datos)
  request.post("http://localhost:5000/iot", json=datos);
  time.sleep(10)