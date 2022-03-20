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

# import all required libraries
import machine
import time
import os
import network
import esp
import onewire
import ds18x20
import lib.sdcard
import ujson as json
import ubinascii
import select
import socket
import gc
gc.collect()

# setup constants
DEBUG = True # keep True to check functioning of code
FAST_BLINK_DURATION_SEC = 0.1 # duration to light LED for fast blinking
SLOW_BLINK_DURATION_SEC = 0.5 # duration to light LED for slow blinking

# storage stuff
DATA_FILENAME = 'DATA_' # set file name
DATA_MAX_FILE_SIZE = 1*1000*1000 # 1M

# thresholds
SLEEP_INTERVAL_SEC = 10 # interval in secs for reading temperature
TEMP_AVG_FREQ = 8       # frequency of averaging temerature and logging
TEMP_EXCEED_LIMIT = 24  # temperate threshold (degrees celcius) to indicate red LED 

# log temperature value
def store_data(filename, data):
    with open(filename, 'a') as outfile:
        if DEBUG:
            print('Writing', filename)
        outfile.write(json.dumps(data) + '\n')
        if DEBUG:
            print('Filesize of', filename,':', outfile.tell())
        return outfile.tell() < DATA_MAX_FILE_SIZE
    return True

# initialize temperature logging file
def create_empty_file(filename):
    if DEBUG:
        print('Creating empty file', filename)
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
    res['time'] = str(time.time())
    return res, temp

def read_stored_data(path='/sd/', remove = False):
    for f in os.listdir(path):
        if f.startswith(DATA_FILENAME):
            print('FILE', f)
            with open(path+f, 'r') as infile:
                for line in infile:
                    print(line, end='')
                print('')
            if remove:
                os.remove(path+f)



# Disable communication first to further reduce energy consumption
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

# pin connection
button = machine.Pin(0, machine.Pin.IN)
led_red = machine.Pin(4, machine.Pin.OUT)
led_green = machine.Pin(5, machine.Pin.OUT)
led = machine.Pin(2, machine.Pin.OUT) # built-in LED

# start indication
for i in range(10):
    led_red.value(not led_red.value())
    led_green.value(not led_red.value())
    time.sleep(SLOW_BLINK_DURATION_SEC)
led_red.value(0)
led_green.value(0)

# Enable one wire temerature sensor
ow = onewire.OneWire(machine.Pin(2))
ow.scan()                # return a list of devices on the bus
ow.reset()               # reset the bus
ds = ds18x20.DS18X20(ow) # get handle

# get handle to SD card for writing and mount as volume
sd = lib.sdcard.SDCard(machine.SPI(1), machine.Pin(15))
os.mount(sd, '/sd')

# number appended to log file name
last_fileid = 0

# find the last number of the last file name
for fn in os.listdir('/sd'):
    try:
        if DEBUG:
            print('Found file:', fn)
        last_fileid = max(last_fileid, int(fn.split('_')[1]))
    except:
        pass
if DEBUG:
    print('fileid', last_fileid)

# variable to keep track of current state
logstarted = False
webstarted = False

# socket details
ssocket = None
poll = None
saddr = None

def interrupt_handler(x):
    global logstarted, webstarted, last_fileid, ssocket, poll, saddr

    # count button press duration
    x = 0
    while button.value()==0:
        time.sleep(1)
        x = x + 1
    
    # check if short press, then log temperature
    if x >= 3 and x <= 7:

        # start temperature logging
        logstarted = True

        # init LEDs
        led_green.value(0)
        led_red.value(0)

        # blink green
        for i in range(6):
            led_green.value(not led_green.value())
            time.sleep(SLOW_BLINK_DURATION_SEC)

        if DEBUG:
            print('starting temperature logging with new file')

        # create new log file and log first temperature
        last_fileid += 1
        filename = '/sd/' + DATA_FILENAME + str(last_fileid)
        if DEBUG:
            print('new file name', filename)
        data = {}
        data['id'] = esp.flash_id()
        data['data'], temp = read_sensors()
        if DEBUG:
            print(data)
        store_data(filename, data)

    # check if long press, then start web server
    if x >= 8:

        # blink red
        for i in range(6):
            led_red.value(not led_red.value())
            time.sleep(SLOW_BLINK_DURATION_SEC)
        led_red.value(0)

        # start or stop WLAN AP and web server
        if not webstarted:

            # say web server and AP is active now
            webstarted = True
            if DEBUG:
                print('starting web server')

            # bring up WLAN AP
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            ap.config(password='navel2021')
            while ap.active() == False:
                pass
            if DEBUG:
                print(ap.ifconfig())

            # set up web server om port 80
            ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            saddr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
            if DEBUG:
                print('server:', saddr)
            ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            ssocket.bind(saddr)
            ssocket.listen(5)
            ssocket.setblocking(False)

            # setup polling based connections
            poll = select.poll()
            poll.register(ssocket, select.POLLIN)
            time.sleep(2)

        else:

            # say web server and AP is not active any more
            webstarted = False
            if DEBUG:
                print('stopping web server')

            # unregister polling
            poll.unregister(ssocket)

            # close socket
            ssocket.close()

            # shutdown WLAN AP
            ap = network.WLAN(network.AP_IF)
            ap.active(False)

# setup button handler (call function)
button.irq(handler=interrupt_handler, trigger=machine.Pin.IRQ_FALLING)

# ring buffer to keep temperature to average
average_list = []

# next temperature logging time
next_logtime = time.time() + SLEEP_INTERVAL_SEC

# start main loop of logging temperature
while True:
    
    # set for light sleep - only if logging started but no web server active
    if logstarted and not webstarted:
        do_lightsleep = True
    else:
        do_lightsleep = False

    # check and do light sleep
    if do_lightsleep:
        machine.lightsleep(SLEEP_INTERVAL_SEC * 1000)

    # log temperature if started (with short press)
    if logstarted and time.time() > next_logtime:

        if DEBUG:
            print('I woke up')

        # blink green
        led_green.value(1)
        time.sleep(FAST_BLINK_DURATION_SEC)
        led_green.value(0)

        # read temperature from sensor
        data = {}
        data['id'] = esp.flash_id()
        data['data'], temp = read_sensors()

        if DEBUG:
            print('after read_sensors')

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
                data['msg'] = ('Threshold of ' + str(TEMP_EXCEED_LIMIT) + ' degrees was crossed')

            # release garbage
            gc.collect()

        if DEBUG:
            print(data)

        # log temperature data and check file size exceeded
        filename = '/sd/' + DATA_FILENAME + str(last_fileid)
        if not store_data(filename, data):

            # create new file for next log if size exceeded
            last_fileid += 1
            filename = '/sd/' + DATA_FILENAME + str(last_fileid)
            create_empty_file(filename)
        
        # setup for next temperature logging time
        next_logtime = time.time() + SLEEP_INTERVAL_SEC

    # serve web pages if web server up
    if webstarted:

        # wait for incoming connections
        status = poll.poll(SLEEP_INTERVAL_SEC * 1000)

        # server pages when there are connections
        if status:
            if DEBUG:
                print('connection request on local address', saddr)
            
            # setup connection to requester
            csocket, caddr = ssocket.accept()
            csocket.setblocking(True)

            # read user web request
            csocketfile = csocket.makefile('rwb', 0)
            if DEBUG:
                print('received:', 'from', caddr, '\n')
            
            # split request data to identify type
            selectfile = None
            while True:
                line = csocketfile.readline()
                if DEBUG:
                    print(line)
                utf8str = line.decode('utf-8')
                if utf8str.startswith('GET') and 'filename=' in utf8str:
                    selectfile = utf8str.split(' ')[1].split('=')[1]
                if not line or line == b'\r\n':
                    break
            
            # check request details decide what page to show
            if not selectfile:
                # show index page with files
                if DEBUG:
                    print('sending index page to', caddr, '\n')

                # get first part of index page
                pagepart = ''
                with open('lib/index-part-1.html', 'r') as fp:
                    pagepart = fp.read()
                csocket.send(pagepart)

                # get files part of index page
                for name in os.listdir('/sd'):
                    pagepart = ('<option value=\"' + name + '\">' + name + '</option>\n')
                    csocket.send(pagepart)

                # get last part of index page
                with open('lib/index-part-2.html', 'r') as fp:
                    pagepart = fp.read()
                    csocket.send(pagepart)
                
                # wait a little
                time.sleep(2)
            else:
                # show contents of selected file
                csocket.sendall('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
                csocket.sendall('[')

                # read file contents line by line to send
                with open('/sd/' + selectfile, 'r') as fp:
                    isfirst = True
                    for line in fp:
                        if not isfirst:
                            csocket.send(',')
                        else:
                            isfirst = False
                        csocket.sendall(line)
                csocket.sendall(']')

            # end session
            csocket.close()

            # release unwanted mem use
            gc.collect()

