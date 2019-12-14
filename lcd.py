# sudo apt-get install python3-pip
# sudo pip3 install adafruit-blinka
# sudo pip3 install adafruit-circuitpython-charlcd



from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

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


# wipe LCD screen before we start
lcd.clear()
lcd.message = "Ho Yea!\nIt's working!!!"
sleep(2)
lcd.clear()

try:
    while True:
        lcd.message = datetime.now().strftime('%b %d  %H:%M:%S')
        sleep(1)

except KeyboardInterrupt:
    lcd.clear()
