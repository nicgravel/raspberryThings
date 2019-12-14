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

# looking for an active Ethernet or WiFi device
def find_interface():
    dev_name = "null"
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

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

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

def show_ip(ip_address):
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')
    lcd_line_2 = "IP " + ip_address
    lcd.message = lcd_line_1 + lcd_line_2

def show_temp():
    lcd.clear()
    lcd.message("Temp")

# wipe LCD screen before we start
bootMsg = "nickPiScript01\n " + "By nicgravel"
lcd.clear()
lcd.message = bootMsg
print(bootMsg)
sleep(2)
curIp = parse_ip(find_interface())
show_ip(curIp)

cntLan = 0
cntShowIp = 0

try:
    while True:
        latestIp = parse_ip(find_interface())
        #if latestIp != curIp and cntLan > 0:

        show_ip(latestIp)

        sleep(1)

except KeyboardInterrupt:
    lcd.clear()
