# Food Safety Prototype

The Food Safety Prototype demonstrates how the resources available at the FAB Lab can be used to develop a solution for a specific use case. The use case relates to transporting meat or milk safely in Cameroon. This README provides details of the scenario, the hardware used and the code of the protype. The following locations have furrther details.

- [Design](./design/) - Contains the flow charts of the prograsm logic, pin assignments, etc.
- [Program code](./code/) - Contains the program code of the prototype



## Scenario

There are a number of different transportation means used by producers of meat and milk to deliver them to the sellers who will further process or sell directly to customers. During the transportation, the products are refrigerated but due to technical reasons, the refrigeration may fail. But, to know whether such a failure occured, there is not control mechanisms adopted.

The idea of this prototype is to build a self contained temperature monitoring device that is able to inform the sellers about the changes of the temperature during transport. The prototype will consit of a visual indicator to indicate whether temperature had exceeded a certain threshold during the transportation. Addition to this indications, the prototype also logs the temperature with time. For further analysis, the sellers can download this information to analyse the behaviour.

The picture below shows the protoype. It consist of the following components.

- Temperature sensor
- Button
- 3 LEDs (Red, Green and Blue)

<p align="center">
    <img src="images/prototype-top.jpg" alt="Prototype from top" width="400"/>
</p>
<p align="center">
    <em>The protype from the top with its temperature sensor against the backdrop of a CR2032 coin battery</em>
</p>

<p align="center">
    <img src="images/prototype-side.jpg" alt="Prototype from side" width="400"/>
</p>
<p align="center">
    <em>The protype from the side where the button and the 3 LEDs are visible</em>
</p>

The operation of the prototype is described by the following setences.

- When the prototype boots up, the <span style="color:red">red</span> LED will blink 3 times to indicate that it is ready for operation.
- When the button is pressed for a short time, between 5 and 7 seconds, the prototype will start logging the temperature. This is also considered as a reset of the system.
- The temperature will be logged every 10 seconds and with a <span style="color:red">green</span> blink of the LED.
- When logging the temperature, if the average temperature from the last 8 readings exceeds a threshold, set to 7 degrees celcius, then the <span style="color:red">red</span> LED will be lit permenently until a reset is done.
- If a long button press is performed, a press between 10 and 15 seconds, the a WLAN access point and a web server is brout up by the protype.
- The user can connect to this WLAN AP and browse the web server to download data.
- A short press would reset the prototype to make it ready for its next use again.


## Hardware

The prototype is based on the `Wemos D1 ESP8266` board placed together with other shields. The list of shields used are as follows.

- Wemos D1 ESP8266 shield
- SD card shield
- Battery shield
- Port explansion shield

The components attached to these sheilds are as follows.

- 3 LEDs (red green and blue)
- DS18S20 one-wire temperature sensor
- Push button
- 3.7V 2600mAh rechargeable battery
- Cables connecting the ports and the components

The picture below shows the prototype opened up.

<p align="center">
    <img src="images/prototype-guts.jpg" alt="Prototype guts" width="500"/>
</p>
<p align="center">
    <em>The prototype open showing all components and connections</em>
</p>

The following table lists the pin assignments of the prototype.

| Pin on Board   | Pin on ESP8266  | Details                                            |
|----------------|-----------------|----------------------------------------------------|
| TX             | TXD             | TXD (don't use)                                    |
| RX             | RXD             | RXD (don't use)                                    |
| A0             | A0              | Analog input, max 3.2V, not used                   |
| D0             | GPIO16          | Connected to RST                                   |
| D1             | GPIO5           | Green LED                                          |
| D2             | GPIO4           | Red LED                                            |
| D3             | GPIO0           | Button -> GND (Pullup)                             |
| D4             | GPIO2           | IO, 10k Pull-up built-in LED, OneWire sensor Data  |
| D5             | GPIO14          | CLK SDcard                                         |
| D6             | GPIO12          | MISO SDcard                                        |
| D7             | GPIO13          | MOSI SDcard                                        |
| D8             | GPIO15          | SS SDcard                                          |
| G              | GND             | Ground                                             |
| 5V             | 5V              | not available                                      |
| 3V3            | 3.3V            | 3.3V connection                                    |
| RST            | RST             | Reset                                              |



## Code

The code of the program consist of a number of parts combining the following activities.

- Reading temperature sensor
- Averaging temperature values to check whether threshold exceeded
- Handling button presses (long press or short press) through an interrupt handler
- Writing to SD card
- Setting up web server with the logged data

The following sections show and describe the code related to the above activities.

#### Reading temperature sensor




```Python

# Enable one wire temerature sensor
ow = onewire.OneWire(machine.Pin(2))
ow.scan()                # return a list of devices on the bus
ow.reset()               # reset the bus
ds = ds18x20.DS18X20(ow) # get handle

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

# read temperature from sensor
data = {}
data["id"] = esp.flash_id()
data["data"], temp = read_sensors()

```

