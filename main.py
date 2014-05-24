import RPi.GPIO as GPIO
import os
import time
import datetime
import subprocess
import re
from AdafruitLibs.Adafruit_I2C import Adafruit_I2C
from AdafruitLibs.Adafruit_7Segment import SevenSegment
from AdafruitLibs.Adafruit_BMP085 import BMP085


def display(txt, colon=False):

    if txt == "time":
        now = datetime.datetime.now()
        _1 = int(now.hour / 10)
        _2 = now.hour % 10
        _3 = int(now.minute / 10)
        _4 = now.minute % 10
        segment.setColon(1)
    else:
        _1 = txt[0]
        _2 = txt[1]
        _3 = txt[2]
        _4 = txt[3]


    segment.writeDigit(0, _1)
    segment.writeDigit(1, _2)
    segment.writeDigit(3, _3)
    segment.writeDigit(4, _4)

    # Toggle colon
    if colon:
        segment.setColon(1)
    else:
        segment.setColon(0)


def countdown(i):

    while(i!=-1):
        display(map(int, str(i).zfill(3)) )
        # Toggle color
        time.sleep(1)
        i-=1


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


def DHT22():
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

def bmpSensor():

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


def readButton(pin):
    GPIO.setup(pin, GPIO.IN)
    if (GPIO.input(pin) == False):
        print("button was pushed")

if __name__ == '__main__':

    but1pin = 22  #change button pin
    but1pin = 24  #change button pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(but1pin, GPIO.IN)
    but1 = GPIO.input(but1pin)
    #GPIO.setup(but2pin, GPIO.IN)
    #but2 = GPIO.input(but2pin)

    #for the display
    segment = SevenSegment(address=0x70)

    bmp = BMP085(0x77)

    while True:

        temp = str(bmp.readTemperature())
        if "." in temp:
            temp = temp.replace(".", "")
        templst = [int(i) for i in temp.zfill(4)]
        display(templst, False)
        time.sleep(4)

        #sudo chmod +x Adafruit_DHT
        rawHum = str(DHT22())
        if "." in rawHum:
            rawHum = rawHum.replace(".", "")
        humlst = [int(i) for i in rawHum.zfill(4)]
        display(humlst)
        time.sleep(4)

        bmp = bmp.readPressure()
        bmplst = [int(i) for i in str(bmp)]
        display(bmplst, False)
        time.sleep(4)

        display("time", True)
        time.sleep(10)

        #temp hack till i have 2 buttons installed
        but2 = True
        if but1 == True and but2 == True:
            import sys
            sys.exit()
