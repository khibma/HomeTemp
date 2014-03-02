import RPi.GPIO as GPIO
import os
import time
import datetime
from .AdafruitLibs.Adafruit_I2C import Adafruit_I2C
from .AdafruitLibs.Adafruit_7Segment import SevenSegment
from .AdafruitLibs.Adafruit_BMP085 import BMP085

GPIO.setmode(GPIO.BCM)

#for the display
segment = SevenSegment(address=0x70)


def countdown(n):
     while n > 0:
        time.sleep(1)
        print (n)
        n = n-1
     print("0000")


def clock():
    while(True):
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
      # Wait one second
      time.sleep(1)

def DHT22():
    os.command("sudo ./AdafruitLibs/Adafruit_DHT_Driver/Adafruit_DHT 22 #")  #update pin #


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


    while True:

        getTemp()
        time.sleep(4)
        getHumidity()
        time.sleep(4)
        getPressure()
        time.sleep(4)


        if but1 == True and but2 == True:
            import sys
            sys.exit()
