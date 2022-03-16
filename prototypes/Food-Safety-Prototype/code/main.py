# Code of the Food Safety Prototype developed
# for the NAVEL project. This protype is based
# on the following hardware.
#
# - Wemos D1 ESP8266 board
# - DS18X20 temperature sensor
# - 3 LEDs (green, red, blue)
# - Button
# - Micro SD shield
# - battery shield and battery
# 
# The purpose of this hardware and program together
# is to sense the temperature when used in the
# 2 scenarios discussed for NAVEL and indicate when
# it exceeds a certain threshold.
#
# This code is based on the wemos/esp8266 data logger
# developed by Jens Dede <jd@comnets.uni-bremen.de>
#
# author: Eenesh Chavan <eenesh.chavan@uni-bremen.de>
# modified: Asanga Udugama <udugama@uni-bremen.de>
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
import lib.sdcard
import ujson as json
import ubinascii
import esp
from lib.webserver import SimpleWebserver

# Disable communication first to further reduce energy consumption
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

# setup constants
DEBUG = False # keep True to check functioning of code

# pin connection
button = machine.Pin(0, machine.Pin.IN)
led_red = machine.Pin(4, machine.Pin.OUT)
led_green = machine.Pin(5, machine.Pin.OUT)
led = machine.Pin(2, machine.Pin.OUT) # built-in LED

# start indication
for i in range(6):
    led_red.value(not led_red.value())
    led_green.value(not led_red.value())
    time.sleep(0.3)
led_red.value(0)
led_green.value(0)

# storage stuff
DATA_FILENAME = "DATA_" # set file name
DATA_MAX_FILE_SIZE = 1*1000*1000 # 1M

# thresholds
SLEEP_INTERVAL_SEC = 10 # interval in secs for reading temperature
TEMP_AVG_FREQ = 8       # frequency of averaging temerature and logging
TEMP_EXCEED_LIMIT = 25  # temperate threshold (degrees) to indicate red LED 

# log temperature value
def store_data(filename, data):
    with open(filename, "a") as outfile:
        if DEBUG:
            print("Writing", filename)
        outfile.write(json.dumps(data) + "\n")
        if DEBUG:
            print("Filesize of", filename,":", outfile.tell())
        return outfile.tell() < DATA_MAX_FILE_SIZE
    return True

# initialize temperature logging file
def create_empty_file(filename):
    if DEBUG:
        print("Creating empty file", filename)
    open(filename, 'a').close()

# read temperature value from sensor
def read_sensors():
    temp = 0
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    res = {}
    for rom in roms:
        temp = ds.read_temp(rom)
        res[ubinascii.hexlify(rom)] = temp
    res["time"] = str(time.time())
    return res, temp

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

# Enable one wire temerature sensor
ow = onewire.OneWire(machine.Pin(2))
ow.scan()                # return a list of devices on the bus
ow.reset()               # reset the bus
ds = ds18x20.DS18X20(ow) # get handle

# get handle to SD card for writing and mount as volume
sd = lib.sdcard.SDCard(machine.SPI(1), machine.Pin(15))
os.mount(sd, '/sd')

# number appended to log file name
new_fileid = 0

# find the last number of the last file name
for fn in os.listdir('/sd'):
    try:
        if DEBUG:
            print("Found file:", fn)
        new_fileid = max(new_fileid, int(fn.split("_")[1]))
    except:
        pass
if DEBUG:
    print("fileid", new_fileid)

# variable to keep track of current state
# i.e., just booted or button pressed to start logging temp
session = 0

def interrupt_handler(x):
    global session, new_fileid

    # count button press duration
    x = 0
    while button.value()==0:
        time.sleep(1)
        x = x + 1
    
    # check if short press, then log temperature
    if 3 <= x <= 7:

        # increment system state variable
        session =+ 1

        # blink green
        for i in range(6):
            led_green.value(not led_green.value())
            time.sleep(0.5)
        led_green.value(0)

        # create new log file and log first temperature
        new_fileid = new_fileid + 1
        filename = "/sd/" + DATA_FILENAME + str(new_fileid)
        if DEBUG:
            print(new_fileid, filename)
        data = {}
        data["id"] = esp.flash_id()
        data["data"], temp = read_sensors()
        if DEBUG:
            print(data)
        store_data(filename, data)

    # check if long press, then start web server
    if 8 <= x <= 12:

        # blink red
        for i in range(4):
            led_red.value(not led_red.value())
            time.sleep(0.5)
        led_red.value(0)

        # start web server
        sws = SimpleWebserver()
        sws.serve()
    

# setup button handler (call function)
button.irq(handler=interrupt_handler, trigger=machine.Pin.IRQ_FALLING)

# ring buffer to keep temperature to average
average_list = []

# start main loop of logging temperature
while True:
    
    # light sleep
    machine.lightsleep(SLEEP_INTERVAL_SEC * 1000)

    # log only if at least once the short press is done
    if session > 0:

        if DEBUG:
            print("I woke up")
        
        # blink green
        led_green.value(1)
        time.sleep(0.1)
        led_green.value(0)

        # read temperature from sensor
        data = {}
        data["id"] = esp.flash_id()
        data["data"], temp = read_sensors()

        # add to list
        average_list.append(temp)

        if DEBUG:
            print('average array elements:', len(average_list), 'values:', average_list)

        # perform threshold check
        if len(average_list) >= TEMP_AVG_FREQ:

            # compute average
            average = sum(average_list)/len(average_list)
            if DEBUG:
                print('average:', average)
            
            # init list
            average_list = []

            # check threshold to light red LED and log
            if average >= TEMP_EXCEED_LIMIT:
                led_red.value(1)
                data[('Threshold of ' + str() + ' degrees was crossed')]
        
        if DEBUG:
            print(data)
        
        # log temperature data and check file size exceeded
        filename = "/sd/" + DATA_FILENAME + str(new_fileid)
        if not store_data(filename, data):

            # create new file for next log if size exceeded
            new_fileid = new_fileid + 1
            filename = "/sd/" + DATA_FILENAME + str(new_fileid)
            create_empty_file(filename)
