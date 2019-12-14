#sudo pip3 install w1thermsensor

import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
sensor.set_precision(9)

while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)