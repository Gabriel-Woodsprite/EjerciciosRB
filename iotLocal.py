from dht11_gpiozero import DHT11Device
import request, time

url = "http://192.168.0.101:5000/datos"

tmpData = DHT11Device(4, poll_interval=2.0)

while True:
    h = tmpData.humidity
    t = tmpData.temperature
    
    postData = {
        "Temperatura": t,
        "Humedad": h
    }
    r = request.post(url, json=postData)
    print(f'Status: {r.status_code}')
    time.sleep(10)