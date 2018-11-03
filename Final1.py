#!/usr/bin/env python
#
# GrovePi Example for using the Grove Light Sensor and the LED together to turn the LED On and OFF if the background light is greater than a threshold.
# Modules:
# 	http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# 	http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License
The MIT License (MIT)
GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import grovepi
import json
from time import sleep
from grovepi import *
from math import isnan

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

# Temp / Hum Sensor is attached to port 7
dht_sensor_port = 7
dht_sensor_type = 0

# Connect the LED to digital port D4
# SIG,NC,VCC,GND
BLed = 4
GLed = 5
RLed = 6


# Turn on LED once sensor exceeds threshold resistance
threshold = 15

grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(BLed,"OUTPUT")
grovepi.pinMode(GLed,"OUTPUT")
grovepi.pinMode(RLed,"OUTPUT")

outputData = []

# I had to add these extra sleep functions to stop the NAN errors
sleep(.1)

while True:
    try:
        sleep(0.5)
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        if sensor_value <= 0: # stops dividing by 0 errors
            resistance = 0
        else:
            resistance = (float)(1023 - sensor_value) * 10 / sensor_value

	# If Light is on, records data
        if resistance > threshold:
            # Send HIGH to switch off LED
            grovepi.digitalWrite(RLed,0)
            grovepi.digitalWrite(GLed,0)
            grovepi.digitalWrite(BLed,0)
	# If light is off, turns off and stop recording
        else:
            [temp, hum] = dht(dht_sensor_port, dht_sensor_type)
            fahr = (temp * 9/5) +32 # celcius to Fahr
            print(fahr, hum)
            t = fahr
            h = hum
            # Send LOW to switch on LED depening on the Temp and Hum
            if fahr > 95:
                grovepi.digitalWrite(RLed,1)
            elif (fahr > 60 and fahr < 85) and (hum < 80):
                grovepi.digitalWrite(GLed,1)
            elif (fahr > 85 and fahr < 95) and (hum < 80):
                grovepi.digitalWrite(BLed,1)
            elif (hum > 80):
                grovepi.digitalWrite(GLed,1)
                grovepi.digitalWrite(BLed,1)
            else:
                print("No Readings!")
            #Sends data to the global array
            outputData.append([t, h])

        #Used for testing purposes
        #print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
	# Sleeps for 1800 seconds, or 30 minutes
        sleep(1800)

    except IOError:
        print ("Error")

    except KeyboardInterrupt:
        print("Program Terminated by User!!!") # Takes keyboard interrupt and ends
        #Turns off lights ones program stops
        grovepi.digitalWrite(GLed,0)
        grovepi.digitalWrite(BLed,0)
        grovepi.digitalWrite(RLed,0)
        break # Ends program  
    

# Setting up to save the data to outputData text file
with open('outputData.json', 'a') as outfile:
    json.dump(outputData, outfile)