EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Module:WeMos_D1_mini U1
U 1 1 608AD3EE
P 1750 1700
F 0 "U1" H 1750 811 50  0000 C CNN
F 1 "WeMos_D1_mini" H 1750 720 50  0000 C CNN
F 2 "Module:WEMOS_D1_mini_light" H 1750 550 50  0001 C CNN
F 3 "https://wiki.wemos.cc/products:d1:d1_mini#documentation" H -100 550 50  0001 C CNN
	1    1750 1700
	1    0    0    -1  
$EndComp
$Comp
L Interface_Expansion:MCP23017_SP U2
U 1 1 608AF473
P 2250 4800
F 0 "U2" H 2250 6081 50  0000 C CNN
F 1 "MCP23017_SP" H 2250 5990 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W7.62mm" H 2450 3800 50  0001 L CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf" H 2450 3700 50  0001 L CNN
	1    2250 4800
	1    0    0    -1  
$EndComp
Text GLabel 1150 550  0    50   Input ~ 0
3V3
Text GLabel 1150 700  0    50   Input ~ 0
5V
Text GLabel 1150 2750 0    50   Input ~ 0
GND
Wire Wire Line
	1150 550  1850 550 
Wire Wire Line
	1850 550  1850 900 
Wire Wire Line
	1650 900  1650 700 
Wire Wire Line
	1650 700  1150 700 
Wire Wire Line
	1750 2500 1750 2750
Wire Wire Line
	1750 2750 1150 2750
Text GLabel 1200 6150 0    50   Input ~ 0
GND
Wire Wire Line
	2250 5900 2250 6150
Wire Wire Line
	2250 6150 1500 6150
Wire Wire Line
	1550 5600 1500 5600
Wire Wire Line
	1500 5600 1500 6150
Connection ~ 1500 6150
Wire Wire Line
	1500 6150 1200 6150
Wire Wire Line
	1550 5500 1500 5500
Wire Wire Line
	1500 5500 1500 5600
Connection ~ 1500 5600
Wire Wire Line
	1550 5400 1500 5400
Wire Wire Line
	1500 5400 1500 5500
Connection ~ 1500 5500
Text GLabel 1150 4000 0    50   Input ~ 0
SDA
Text GLabel 1150 4100 0    50   Input ~ 0
SCL
Wire Wire Line
	1550 4100 1500 4100
Wire Wire Line
	1550 4000 1250 4000
Text GLabel 2400 1500 2    50   Input ~ 0
SDA
Text GLabel 2400 1400 2    50   Input ~ 0
SCL
Wire Wire Line
	2400 1400 2150 1400
Wire Wire Line
	2400 1500 2150 1500
Text GLabel 1150 3450 0    50   Input ~ 0
3V3
$Comp
L Device:R R1
U 1 1 608BB226
P 1250 3700
F 0 "R1" H 1320 3746 50  0000 L CNN
F 1 "1k" H 1320 3655 50  0000 L CNN
F 2 "" V 1180 3700 50  0001 C CNN
F 3 "~" H 1250 3700 50  0001 C CNN
	1    1250 3700
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 608BB9CB
P 1500 3700
F 0 "R2" H 1570 3746 50  0000 L CNN
F 1 "1k" H 1570 3655 50  0000 L CNN
F 2 "" V 1430 3700 50  0001 C CNN
F 3 "~" H 1500 3700 50  0001 C CNN
	1    1500 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	1150 3450 1250 3450
Wire Wire Line
	1250 3450 1250 3550
Wire Wire Line
	1500 3550 1500 3450
Wire Wire Line
	1500 3450 1250 3450
Connection ~ 1250 3450
Wire Wire Line
	1500 3850 1500 4100
Connection ~ 1500 4100
Wire Wire Line
	1500 4100 1150 4100
Wire Wire Line
	1250 3850 1250 4000
Connection ~ 1250 4000
Wire Wire Line
	1250 4000 1150 4000
Text GLabel 1300 4900 0    50   Input ~ 0
3V
Wire Wire Line
	1300 4900 1550 4900
$Comp
L Connector:Micro_SD_Card J1
U 1 1 608D732E
P 4700 2100
F 0 "J1" H 4650 2817 50  0000 C CNN
F 1 "Micro_SD_Card" H 4650 2726 50  0000 C CNN
F 2 "" H 5850 2400 50  0001 C CNN
F 3 "http://katalog.we-online.de/em/datasheet/693072010801.pdf" H 4700 2100 50  0001 C CNN
	1    4700 2100
	1    0    0    -1  
$EndComp
Text GLabel 5800 2700 2    50   Input ~ 0
GND
Text GLabel 2400 1900 2    50   Input ~ 0
MISO
Text GLabel 2400 2000 2    50   Input ~ 0
MOSI
Text GLabel 2400 2100 2    50   Input ~ 0
SD_CS
Text GLabel 2400 1800 2    50   Input ~ 0
SCK
Wire Wire Line
	2150 1800 2400 1800
Wire Wire Line
	2400 1900 2150 1900
Wire Wire Line
	2150 2000 2400 2000
Text GLabel 3600 2300 0    50   Input ~ 0
GND
Text GLabel 3600 2100 0    50   Input ~ 0
3V3
Text GLabel 3600 2200 0    50   Input ~ 0
SCK
Text GLabel 3600 2000 0    50   Input ~ 0
MOSI
Text GLabel 3600 1900 0    50   Input ~ 0
SD_CS
Wire Wire Line
	3600 1900 3800 1900
Wire Wire Line
	3800 2000 3600 2000
Wire Wire Line
	3600 2100 3800 2100
Wire Wire Line
	3800 2200 3600 2200
Wire Wire Line
	3600 2300 3800 2300
Wire Wire Line
	5500 2700 5800 2700
Text GLabel 3600 2400 0    50   Input ~ 0
MISO
Wire Wire Line
	3600 2400 3800 2400
$Comp
L Timer_RTC:RV-8523-C3 U3
U 1 1 608E8ADB
P 7400 1150
F 0 "U3" H 7400 661 50  0000 C CNN
F 1 "RV-8523-C3" H 7400 570 50  0000 C CNN
F 2 "Package_SON:RTC_SMD_MicroCrystal_C3_2.5x3.7mm" H 8400 800 50  0001 C CNN
F 3 "https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-8523-C3.pdf" H 7400 1150 50  0001 C CNN
	1    7400 1150
	1    0    0    -1  
$EndComp
Text GLabel 6700 950  0    50   Input ~ 0
SCL
Text GLabel 6700 1050 0    50   Input ~ 0
SDA
Text GLabel 7300 1900 0    50   Input ~ 0
GND
Text GLabel 7200 550  0    50   Input ~ 0
3V3
Text GLabel 7200 550  0    50   Input ~ 0
3V3
Wire Wire Line
	7200 550  7300 550 
Wire Wire Line
	7300 550  7300 750 
Wire Wire Line
	7400 1550 7400 1900
Wire Wire Line
	7400 1900 7300 1900
Wire Wire Line
	6900 950  6700 950 
Wire Wire Line
	6700 1050 6900 1050
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 608F001C
P 3850 800
F 0 "J2" H 3930 792 50  0000 L CNN
F 1 "Conn_01x02" H 3930 701 50  0000 L CNN
F 2 "" H 3850 800 50  0001 C CNN
F 3 "~" H 3850 800 50  0001 C CNN
	1    3850 800 
	1    0    0    -1  
$EndComp
Text GLabel 3550 800  0    50   Input ~ 0
D0
Text GLabel 3550 900  0    50   Input ~ 0
RESET
Wire Wire Line
	3650 800  3550 800 
Wire Wire Line
	3550 900  3650 900 
Text GLabel 2400 1300 2    50   Input ~ 0
D0
Text GLabel 1150 1300 0    50   Input ~ 0
RESET
Wire Wire Line
	2400 1300 2150 1300
Wire Wire Line
	1350 1300 1150 1300
Wire Wire Line
	2950 4900 3300 4900
Wire Wire Line
	3900 5000 3550 5000
Wire Wire Line
	2950 5100 3800 5100
$Comp
L Device:R R3
U 1 1 608FBDD6
P 3300 5050
F 0 "R3" H 3370 5096 50  0000 L CNN
F 1 "1k" H 3370 5005 50  0000 L CNN
F 2 "" V 3230 5050 50  0001 C CNN
F 3 "~" H 3300 5050 50  0001 C CNN
	1    3300 5050
	1    0    0    -1  
$EndComp
Connection ~ 3300 4900
Wire Wire Line
	3300 4900 3900 4900
$Comp
L Device:R R4
U 1 1 608FC9A2
P 3550 5150
F 0 "R4" H 3620 5196 50  0000 L CNN
F 1 "1k" H 3620 5105 50  0000 L CNN
F 2 "" V 3480 5150 50  0001 C CNN
F 3 "~" H 3550 5150 50  0001 C CNN
	1    3550 5150
	1    0    0    -1  
$EndComp
Connection ~ 3550 5000
Wire Wire Line
	3550 5000 2950 5000
$Comp
L Device:R R5
U 1 1 608FCF1B
P 3800 5250
F 0 "R5" H 3870 5296 50  0000 L CNN
F 1 "1k" H 3870 5205 50  0000 L CNN
F 2 "" V 3730 5250 50  0001 C CNN
F 3 "~" H 3800 5250 50  0001 C CNN
	1    3800 5250
	1    0    0    -1  
$EndComp
Connection ~ 3800 5100
Wire Wire Line
	3800 5100 3900 5100
Text GLabel 4050 5600 2    50   Input ~ 0
GND
Wire Wire Line
	3300 5200 3300 5600
Wire Wire Line
	3300 5600 3550 5600
Wire Wire Line
	3550 5300 3550 5600
Connection ~ 3550 5600
Wire Wire Line
	3550 5600 3800 5600
Wire Wire Line
	3800 5400 3800 5600
Connection ~ 3800 5600
Wire Wire Line
	3800 5600 4050 5600
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J3
U 1 1 60904032
P 4100 5000
F 0 "J3" H 4150 5317 50  0000 C CNN
F 1 "Conn_02x03_Counter_Clockwise" H 4150 5226 50  0000 C CNN
F 2 "" H 4100 5000 50  0001 C CNN
F 3 "~" H 4100 5000 50  0001 C CNN
	1    4100 5000
	1    0    0    -1  
$EndComp
Text GLabel 4700 5000 2    50   Input ~ 0
3V3
Wire Wire Line
	4400 5000 4550 5000
Wire Wire Line
	4400 4900 4550 4900
Wire Wire Line
	4550 4900 4550 5000
Connection ~ 4550 5000
Wire Wire Line
	4550 5000 4700 5000
Wire Wire Line
	4400 5100 4550 5100
Wire Wire Line
	4550 5100 4550 5000
$Comp
L Connector_Generic:Conn_02x03_Counter_Clockwise J4
U 1 1 60908CD6
P 4050 4100
F 0 "J4" H 4100 4417 50  0000 C CNN
F 1 "Conn_02x03_Counter_Clockwise" H 4100 4326 50  0000 C CNN
F 2 "" H 4050 4100 50  0001 C CNN
F 3 "~" H 4050 4100 50  0001 C CNN
	1    4050 4100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R8
U 1 1 60909C79
P 3400 3750
F 0 "R8" V 3193 3750 50  0000 C CNN
F 1 "220" V 3284 3750 50  0000 C CNN
F 2 "" V 3330 3750 50  0001 C CNN
F 3 "~" H 3400 3750 50  0001 C CNN
	1    3400 3750
	0    1    1    0   
$EndComp
$Comp
L Device:R R7
U 1 1 6090A29E
P 3400 4100
F 0 "R7" V 3193 4100 50  0000 C CNN
F 1 "220" V 3284 4100 50  0000 C CNN
F 2 "" V 3330 4100 50  0001 C CNN
F 3 "~" H 3400 4100 50  0001 C CNN
	1    3400 4100
	0    1    1    0   
$EndComp
$Comp
L Device:R R6
U 1 1 6090A8F4
P 3400 4400
F 0 "R6" V 3193 4400 50  0000 C CNN
F 1 "220" V 3284 4400 50  0000 C CNN
F 2 "" V 3330 4400 50  0001 C CNN
F 3 "~" H 3400 4400 50  0001 C CNN
	1    3400 4400
	0    1    1    0   
$EndComp
Wire Wire Line
	2950 4000 3100 4000
Wire Wire Line
	3100 4000 3100 3750
Wire Wire Line
	3100 3750 3250 3750
Wire Wire Line
	3550 3750 3750 3750
Wire Wire Line
	3750 3750 3750 4000
Wire Wire Line
	3750 4000 3850 4000
Wire Wire Line
	2950 4100 3250 4100
Wire Wire Line
	3550 4100 3850 4100
Wire Wire Line
	2950 4200 3150 4200
Wire Wire Line
	3150 4200 3150 4400
Wire Wire Line
	3150 4400 3250 4400
Wire Wire Line
	3550 4400 3600 4400
Wire Wire Line
	3600 4400 3600 4200
Wire Wire Line
	3600 4200 3850 4200
Text GLabel 4650 4100 2    50   Input ~ 0
GND
Wire Wire Line
	4350 4100 4500 4100
Wire Wire Line
	4350 4000 4500 4000
Wire Wire Line
	4500 4000 4500 4100
Connection ~ 4500 4100
Wire Wire Line
	4500 4100 4650 4100
Wire Wire Line
	4350 4200 4500 4200
Wire Wire Line
	4500 4200 4500 4100
Wire Wire Line
	2400 2100 2150 2100
Text GLabel 2400 1700 2    50   Input ~ 0
ONE_WIRE
$Comp
L Connector_Generic:Conn_01x03 J5
U 1 1 609BAF9B
P 5750 850
F 0 "J5" H 5830 892 50  0000 L CNN
F 1 "Conn_01x03" H 5830 801 50  0000 L CNN
F 2 "" H 5750 850 50  0001 C CNN
F 3 "~" H 5750 850 50  0001 C CNN
	1    5750 850 
	1    0    0    -1  
$EndComp
Text GLabel 5050 750  0    50   Input ~ 0
3V3
Text GLabel 5050 850  0    50   Input ~ 0
ONE_WIRE
Text GLabel 5050 950  0    50   Input ~ 0
GND
$Comp
L Device:R 4k7
U 1 1 609C3D84
P 5300 550
F 0 "4k7" H 5370 596 50  0000 L CNN
F 1 "R9" H 5370 505 50  0000 L CNN
F 2 "" V 5230 550 50  0001 C CNN
F 3 "~" H 5300 550 50  0001 C CNN
	1    5300 550 
	0    1    1    0   
$EndComp
Wire Wire Line
	5150 550  5150 750 
Wire Wire Line
	5050 750  5150 750 
Connection ~ 5150 750 
Text Notes 2850 1650 0    50   ~ 0
D3 / GPIO0 = Boot mode
Text Notes 2850 1750 0    50   ~ 0
D4 / GPIO2 = LED_buildin
Wire Wire Line
	5150 750  5550 750 
Wire Wire Line
	5050 850  5450 850 
Wire Wire Line
	5050 950  5550 950 
Wire Wire Line
	5450 550  5450 850 
Connection ~ 5450 850 
Wire Wire Line
	5450 850  5550 850 
$Comp
L power:+3.3V #PWR0101
U 1 1 60A03B7D
P 2100 700
F 0 "#PWR0101" H 2100 550 50  0001 C CNN
F 1 "+3.3V" H 2115 873 50  0000 C CNN
F 2 "" H 2100 700 50  0001 C CNN
F 3 "" H 2100 700 50  0001 C CNN
	1    2100 700 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 700  2100 900 
Wire Wire Line
	2100 900  1850 900 
Connection ~ 1850 900 
$Comp
L power:GND #PWR0102
U 1 1 60A0BD62
P 1750 2950
F 0 "#PWR0102" H 1750 2700 50  0001 C CNN
F 1 "GND" H 1755 2777 50  0000 C CNN
F 2 "" H 1750 2950 50  0001 C CNN
F 3 "" H 1750 2950 50  0001 C CNN
	1    1750 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1750 2950 1750 2750
Connection ~ 1750 2750
Text GLabel 2050 3400 0    50   Input ~ 0
3V3
Wire Wire Line
	2250 3700 2250 3400
Wire Wire Line
	2250 3400 2050 3400
Wire Wire Line
	2150 1700 2400 1700
$EndSCHEMATC
