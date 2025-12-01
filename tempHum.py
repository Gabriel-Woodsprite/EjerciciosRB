# dht_test.py
from dht11_gpiozero import DHT11Device
import time

s = DHT11Device(4, poll_interval=2.0)

def on_update(dev):
    print("Updated: temp=", dev.temperature, "hum=", dev.humidity)

s.when_updated = on_update

try:
    while True:
        print("Temp:", s.temperature, "Hum:", s.humidity)
        time.sleep(2)
except KeyboardInterrupt:
    s.close()
    print("bye")
