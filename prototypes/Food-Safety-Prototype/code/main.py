# Python script for wemos / esp8266 data logger
#
# Jens Dede, University of Bremen, <jd@comnets.uni-bremen.de>
#
# TODO
# - Add button handler from https://github.com/ComNets-Bremen/wemos-logger
#

"""
PINs and usage

TX 	TXD 	TXD (don't use)
RX 	RXD 	RXD (don't use)
A0 	Analog input, max 3.2V 	A0 (not used)
D0 =  GPIO16 = (connected to RST)
D1 	= GPIO5 = Green LED
D2 = GPIO4  = Red Led
D3 = GPIO0   = Button -> GND (Pullup)
D4 	= GPIO2, IO, 10k Pull-up = BUILTIN_LED,= OneWire sensor Data 	
D5 = GPIO14  = CLK SDcard
D6 = GPIO12  = MISO SDcard
D7 = GPIO13  = MOSI SDcard
D8 = GIO15   = SS SDcard
G 	Ground 	GND
5V 	5V 	-
3V3 	3.3V 	3.3V
RST 	Reset 	RST
"""

import machine
import time
import onewire
import ds18x20
import os
import network
import sdcard
import ujson as json
import ubinascii
import esp
from webserver import SimpleWebserver

# Disable communication first to further reduce energy consumption
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

DEBUG = False # keep True to check functioning of code
DEEPSLEEP = False # deep sleep to save power consumption, doesn't maintain GPIO state
LIGHTSLEEP = True # light sleep mode, maintains GPIO state

# pin connection
button = machine.Pin(0, machine.Pin.IN)
led_red = machine.Pin(4, machine.Pin.OUT)
led_green = machine.Pin(5, machine.Pin.OUT)
led = machine.Pin(2, machine.Pin.OUT) # built-in LED

# start indication
led_red.value(1)
led_green.value(0)
time.sleep(0.3)
led_red.value(0)
led_green.value(1)
time.sleep(0.3)
led_red.value(1)
led_green.value(0)
time.sleep(0.3)
led_red.value(0)
led_green.value(1)
time.sleep(0.3)
led_red.value(1)
led_green.value(0)
time.sleep(0.3)
led_red.value(0)
led_green.value(1)
time.sleep(0.3)
led_red.value(0)
led_green.value(0)

# storage stuff
DATA_FILENAME = "DATA_" # set file name
DATA_MAX_FILE_SIZE = 1*1000*1000 # 1M
INTERVAL = 600 # interval in secs for reding and logging

def store_data(filename, data):
    with open(filename, "a") as outfile:
        print("Writing", filename)
        outfile.write(json.dumps(data) + "\n")
        print("Filesize of", filename,":", outfile.tell())
        return outfile.tell() < DATA_MAX_FILE_SIZE

def create_empty_file(filename):
    print("Creating empty file", filename)
    open(filename, 'a').close()

def read_sensors():
    global temp
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    res = {}
    for rom in roms:
        temp = ds.read_temp(rom)
        res[ubinascii.hexlify(rom)] = temp
    res["time"] = str(time.time())
    return res

def read_stored_data(path="/sd/", remove = False):
    for f in os.listdir(path):
        if f.startswith(DATA_FILENAME):
            print("FILE ", f)
            with open(path+f, "r") as infile:
                for line in infile:
                    print(line, end="")
                print("")
            if remove:
                os.remove(path+f)

# Enable one wire sensor
ow = onewire.OneWire(machine.Pin(2))
ow.scan()               # return a list of devices on the bus
ow.reset()              # reset the bus

ds = ds18x20.DS18X20(ow)

# data reading and logging stuff
sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))

#file directory
os.mount(sd, '/sd')

new_fileid = 0

for fn in os.listdir('/sd'):
    try:
        if DEBUG:
            print("Found file:", fn)
        new_fileid = max(new_fileid, int(fn.split("_")[1]))
    except:
        pass

print("fileid", new_fileid)

filename = None

session = 0 #variable for session state

def interrupt_handler(x):
    global session, new_fileid
    x = 0
    while button.value()==0:
        time.sleep(1)
        x = x + 1
    if 3 <= x <= 7:
        #session start
        session =+ 1
        led_green.value(1)
        time.sleep(0.1)
        led_green.value(0)
        time.sleep(0.1)
        led_green.value(1)
        time.sleep(0.1)
        led_green.value(0)
        time.sleep(0.1)
        led_green.value(1)
        time.sleep(0.1)
        led_green.value(0)
        new_fileid = new_fileid + 1
        filename = "/sd/" + DATA_FILENAME + str(new_fileid)
        print(new_fileid, filename)
        data = {}
        data["id"] = esp.flash_id()
        data["data"] = read_sensors()
        print(data)
        if not store_data(filename, data):
        # Exceeded file limit
            new_fileid = new_fileid + 1
            filename = "/sd/" + DATA_FILENAME + str(new_fileid)
            create_empty_file(filename)
        #machine.lightsleep(10000)
    if 8 <= x <= 12:
        led_red.value(1)
        time.sleep(0.5)
        led_red.value(0)
        time.sleep(0.2)
        led_red.value(1)
        time.sleep(0.5)
        led_red.value(0)
        sws = SimpleWebserver()
        sws.serve()
    


button.irq(handler=interrupt_handler, trigger=machine.Pin.IRQ_FALLING)

average_list = []

while True:
    machine.lightsleep(10000)        
    if session > 0:
        print("I woke up")
        led_green.value(1)
        time.sleep(0.1)
        led_green.value(0)
        data = {}
        data["id"] = esp.flash_id()
        data["data"] = read_sensors()
        if len(average_list) < 8:
            average_list = average_list + [temp]
        print('array of 7 values:', average_list)
        if len(average_list)==7:
            average = sum(average_list)/len(average_list)
            print('average of last 7 values:', average)
            average_list.clear()
            if average > 25:
                led_red.value(1)
                data["threshold was crossed here"]
        
        print(data)
        filename = "/sd/" + DATA_FILENAME + str(new_fileid)
        if not store_data(filename, data):
        # Exceeded file limit
            new_fileid = new_fileid + 1
            filename = "/sd/" + DATA_FILENAME + str(new_fileid)
            create_empty_file(filename)
        #if LIGHTSLEEP:
            #machine.lightsleep(10000)
            
        
        



