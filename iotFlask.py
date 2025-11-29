import requests
import time
url = "http://localhost:5000/index"

while True:
  datos = {"Temperatora":22, "Humedad":50}
  requests.post(url, json=datos)
  time.sleep(5)
  