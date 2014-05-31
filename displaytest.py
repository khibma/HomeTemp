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
        self.time = self.getTime()

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


    def getTime(self):
        now = datetime.datetime.now()
        print "time    {}".format(now)
        return now


def display(txt, colon=False):

    segment.setColon(False)
    # If colon, displaying time..
    if colon:
        digits = []
        digits.append(int(txt.hour / 10))
        digits.append(txt.hour % 10)
        digits.append(int(txt.minute / 10))
        digits.append(txt.minute % 10)
        dotIdx = 0
        segment.setColon(True)
    else:
        dotIdx = txt.find('.')
        if dotIdx > 0:
            txt = txt.replace(".", "")
        digits = list(txt)
        #templst = [int(i) for i in temp.zfill(4)]
    for i in range(0,3):
        dot= False
        if dotIdx >0:
            if i == dotIdx:
                dot=True
                print "dotidx: {}".format(dot)
        print "insert at: {}  value: {} ".format(i, digits[i])
        if digits[i] == 'c' or digits[i] == 'h':
            segment.writeDigitRaw(i, digits[i])
        else:
            segment.writeDigit(i, int(digits[i]), dot)


if __name__ == '__main__':

    #Setup
    bmp = BMP085(0x77)
    DHTPIN = "25"
    BUT1PIN = 22
    BUT2PIN = 24

    #Init the display
    segment = SevenSegment(address=0x70)

    #Ready the sensors

    segment.writeDigit(0, 1, True)
    segment.writeDigit(1, 2)
    segment.writeDigit(3, True)
    segment.writeDigit(4, 4)
    time.sleep(3)
    segment.clear()
    time.sleep(1)
    segment.writeDigitRaw(1, 1)
    time.sleep(1)
    segment.writeDigitRaw(1, 2)
    time.sleep(1)
    segment.writeDigitRaw(1, 4)
    time.sleep(1)
    segment.writeDigitRaw(1, 8)
    time.sleep(1)
    segment.writeDigitRaw(1, 64)
    time.sleep(1)
    segment.writeDigitRaw(1, 4096)



    for i in range(0,100):
        segment.writeDigitRaw(1, i)
        raw_input("press enter")


    time.sleep(1)
    segment.writeDigitRaw(1, 2)
    time.sleep(1)
    segment.writeDigitRaw(1, 3)
    time.sleep(1)
    segment.writeDigitRaw(1, 4)
    time.sleep(1)
    segment.writeDigitRaw(1, 5)
    time.sleep(1)
    segment.writeDigitRaw(1, 6)
    time.sleep(1)
    segment.writeDigitRaw(1, 7)
    time.sleep(1)
    segment.writeDigitRaw(1, 8)
    time.sleep(1)
    segment.writeDigitRaw(1, 9)
    time.sleep(1)
    segment.writeDigitRaw(1, 10)
    time.sleep(1)
    segment.writeDigitRaw(1, 11)
    time.sleep(1)
    segment.writeDigitRaw(1, 12)
    time.sleep(1)
    segment.writeDigitRaw(1, 13)
    time.sleep(1)
    segment.writeDigitRaw(1, 14)
    time.sleep(1)
    segment.writeDigitRaw(1, 15)
    time.sleep(1)
    segment.writeDigitRaw(1, 16)
    time.sleep(1)
    segment.writeDigitRaw(1, 17)
    time.sleep(1)
    segment.writeDigitRaw(1, 18)
    time.sleep(1)
    segment.writeDigitRaw(1, 19)
    time.sleep(1)
    segment.writeDigitRaw(1, 20)