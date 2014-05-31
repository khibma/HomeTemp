import RPi.GPIO as GPIO
import os
import sys
import time
import datetime
import subprocess
import re
from AdafruitLibs.Adafruit_I2C import Adafruit_I2C
from AdafruitLibs.Adafruit_7Segment import SevenSegment
from AdafruitLibs.Adafruit_BMP085 import BMP085

class SensorValues(object):

    def __init__(self, bmp, DHTPIN, BUT1PIN, BUT2PIN):
        self.bmp = bmp
        self.temp = self.getTemp()
        self.humidity = self.getHum(DHTPIN)
        self.pressure = self.getPressure()

    def getTemp(self):
        temp = str(self.bmp.readTemperature())
        print "temp:   {}".format(temp)
        return temp

    def getHum(self, DHTPIN):
        while True:
            try:
                output = subprocess.check_output(["./AdafruitLibs/Adafruit_DHT_Driver/Adafruit_DHT", "22", DHTPIN]);
                matches = re.search("Hum =\s+([0-9.]+)", output)
                humidity = str(float(matches.group(1)))
                print "humidity    {}".format(humidity)
                return humidity
            except:
                time.sleep(1)

    def getPressure(self):
        pressure = self.bmp.readPressure()
        print "pressure    {}".format(pressure)
        return pressure

def display(txt, colon=False):

    segment.setColon(False)
    # If colon, displaying time..
    if colon == True:
        digits = []
        digits.append(int(txt.hour / 10))
        digits.append(txt.hour % 10)
        digits.append(int(txt.minute / 10))
        digits.append(txt.minute % 10)
        dotIdx = 0
        segment.setColon(True)
    else:
        dotIdx = txt.find('.')-1
        if dotIdx > 0:
            txt = txt.replace(".", "")

        digits = list(txt)
        segment.setColon(False)
        print digits

        #templst = [int(i) for i in temp.zfill(4)]
    digits.insert(2,0) #colon is postion 2, so insert a dummy value
    if dotIdx >=2:
        dotIdx+=1

    for i in range(0,5):
        if i == 2:
            continue

        dot = False
        if dotIdx >0:
            if i == dotIdx:
                dot = True
        print "insert at: {}  value: {} ".format(i, digits[i])

        if digits[i] == 'c':
            segment.writeDigitRaw(i, 99)
        elif digits[i] == 'h':
            segment.writeDigitRaw(i, 116)
        else:
            segment.writeDigit(i, int(digits[i]), dot)
            print dot


def countdown(i):

    while(i!=-1):
        display(map(int, str(i).zfill(3)) )
        time.sleep(1)
        i-=1


def readButton(pin):
    GPIO.setup(pin, GPIO.IN)
    if (GPIO.input(pin) == False):
        print("button was pushed")

if __name__ == '__main__':

    #Setup
    bmp = BMP085(0x77)
    DHTPIN = "25"
    BUT1PIN = 22
    BUT2PIN = 24

    #Init the display
    segment = SevenSegment(address=0x70)

    #Ready the sensors
    sensor = SensorValues(bmp, DHTPIN, BUT1PIN, BUT2PIN)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUT1PIN, GPIO.IN)
    but1 = GPIO.input(BUT1PIN)
    #GPIO.setup(BUT2PIN, GPIO.IN)
    #but2 = GPIO.input(BUT2PIN)

    while True:

        display(str(sensor.temp)+'c', False)
        time.sleep(4)

        display(str(sensor.humidity)+'h', False)
        time.sleep(4)

        display(str(sensor.pressure), False)
        time.sleep(4)

        display(datetime.datetime.now(), True)
        time.sleep(6)

        #temp hack till i have 2 buttons installed
        but2 = False
        if but1 == True and but2 == True:
            sys.exit()




'''NOT USED'''
def _bmpSensor():

    bmp = BMP085(0x77)

    # To specify a different operating mode, uncomment one of the following:
    # bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
    # bmp = BMP085(0x77, 1)  # STANDARD Mode
    # bmp = BMP085(0x77, 2)  # HIRES Mode
    # bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode

    temp = bmp.readTemperature()

    # Read the current barometric pressure level
    pressure = bmp.readPressure()

    # To calculate altitude based on an estimated mean sea level pressure
    # (1013.25 hPa) call the function as follows, but this won't be very accurate
    altitude = bmp.readAltitude()

    # To specify a more accurate altitude, enter the correct mean sea level
    # pressure level.  For example, if the current pressure level is 1023.50 hPa
    # enter 102350 since we include two decimal places in the integer value
    # altitude = bmp.readAltitude(102350)

    print ("Temperature: {0:2} C").format(temp)
    print ("Pressure:    {0:2} hPa").format(pressure / 100.0)
    print ("Altitude:    {0:2}").format(altitude)


def clock():
    #not used
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    # Set hours
    segment.writeDigit(0, int(hour / 10))     # Tens
    segment.writeDigit(1, hour % 10)          # Ones
    # Set minutes
    segment.writeDigit(3, int(minute / 10))   # Tens
    segment.writeDigit(4, minute % 10)        # Ones
    # Toggle color
    segment.setColon(second % 2)              # Toggle colon at 1Hz


def _DHT22():
    #os.command("sudo ./AdafruitLibs/Adafruit_DHT_Driver/Adafruit_DHT 22 25")  #update pin # at the end

    print "everything here inside DHT22"
    output = subprocess.check_output(["./AdafruitLibs/Adafruit_DHT_Driver/Adafruit_DHT", "22", "25"]);
    print output
    matches = re.search("Temp =\s+([0-9.]+)", output)
    temp = float(matches.group(1))

    # search for humidity printout
    matches = re.search("Hum =\s+([0-9.]+)", output)
    humidity = float(matches.group(1))


    print "Temperature: %.1f C" % temp
    print "Humidity:    %.1f %%" % humidity
    return humidity