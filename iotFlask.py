import requests
import time

url = "http://192.168.0.101:5000/datos"  # Cambia esto por la IP de tu servidor Flask

while True:
    datos = {
        "temperatura": 22,
        "humedad": 50
    }

    try:
        r = requests.post(url, json=datos)
        print(f'Status: {r.status_code}')
    except Exception as e:
        print("Error enviando datos:", e)

    time.sleep(5)
