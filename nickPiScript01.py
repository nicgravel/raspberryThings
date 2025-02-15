# Need to install dependencies 
#   sudo apt-get install python3-pip
#   sudo pip3 install adafruit-blinka
#   sudo pip3 install adafruit-circuitpython-charlcd
#   sudo pip3 install w1thermsensor
#   sudo python3 -m pip install influxdb (influxDb should be installed and configured)

# DS18B20 temperature sensor connected to GPIO4 (pin 7), 3.3v and gnd

#       LCD PIN            Rasp GPIO   Rasp V.B pin
#------------------------------------------------------
#   LCD Pin #4  (RS)         #22        (pin 13)
#   LCD Pin #6  (EN)         #17        (pin 11)
#   LCD Pin #11 (D4)         #25        (pin 22)
#   LCD Pin #12 (D5)         #24        (pin 18)
#   LCD Pin #13 (D6)         #23        (pin 16)
#   LCD Pin #14 (D7)         #18        (pin 12)
#   LCD Pin #1  (GND)        GND        (pin 6 )
#   LCD Pin #2  (5V)         5V         (pin 2 )


# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from time import sleep
import datetime
from w1thermsensor import W1ThermSensor
from influxdb import InfluxDBClient
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import asyncio


# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)


# Set required InfluxDB parameters.
# (this could be added to the program args instead of beeing hard coded...)
host = "localhost" #Could also use local ip address like "192.168.1.136"
port = 8086
user = "pi"
password = "pi"
dbname = "temperature_db"

# Initialize the Influxdb client
client = InfluxDBClient(host, port, user, password, dbname)

# Initialize DS18B20 temperature prob
sensor = W1ThermSensor()

# Only set the precision one time for the sensor. writing is limited
# sensor.set_precision(9, persist=True) 

# looking for an active Ethernet or WiFi device
def find_interface():
    device_name = "null"
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            device_name = line.split(':')[1]
    return device_name

# find an active IP on the first LIVE network device
def parse_ip(interface):
    ip = "not found"
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

def getIp():
    return parse_ip(find_interface())


# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

def saveToDb(temperature):
    timestamp=datetime.datetime.utcnow().isoformat()

    datapoints = [
        {
            "measurement": "temperature",
            "time": timestamp,
            "fields": {
                "value": temperature
            }
        }
        ]
    
    return client.write_points(datapoints)


# wipe LCD screen before we start
lcd.clear()
lcd.message = "nickPiScript01\n " + "By nicgravel"
sleep(2)
temperature = sensor.get_temperature()
loopCounter = 60
line2 = ""
ip = "not found"


try:
    while True:
        temperature = sensor.get_temperature()

        temperatureText = str(temperature) + " " + chr(223) + "C"
        line1 = datetime.datetime.now().strftime('%b %d  %H:%M:%S\n')

        # Save only each 60 seconds
        if loopCounter == 60:
            lcd.clear()
            line2 = "IP " + getIp()
        elif loopCounter < 58 and loopCounter > 0:
            if loopCounter == 57:
                lcd.clear()
            line2 = temperatureText + "       " + "{:02d}".format(loopCounter) #Display number with leading zeros
        elif loopCounter == 0:
            saveToDb(temperature)
            line2 = temperatureText + " Saving..."
            print("Saving " +  temperatureText)
        elif loopCounter == -1:
            loopCounter = 61
        
        print(line1 + line2 + "\n")
        lcd.message = line1 + line2
        
        loopCounter -= 1

        # Getting the temperature take about one second so we don't have to sleep
        # sleep(1)

except KeyboardInterrupt:
    lcd.clear()

