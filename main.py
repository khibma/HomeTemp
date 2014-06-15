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

import outsideWeather as weather

class SensorValues(object):

    def __init__(self, DHTPIN, BRIGHTPIN, BUT1PIN, BUT2PIN):
        self.bmp = BMP085(0x77)  #BMP-085 sensor
        self.temp = self.getTemp()
        self.humidity = self.getHum(DHTPIN)
        self.pressure = self.getPressure()
        self.brightness = self.checkBrightness(BRIGHTPIN)

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

    def checkBrightness(self, BRIGHTPIN):
        ''' sensor hardware not implemented
        reading = 0
        GPIO.setup(BRIGHTPIN, GPIO.OUT)
        GPIO.output(BRIGHTPIN, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(BRIGHTPIN, GPIO.IN)
        while (GPIO.input(BRIGHTPIN) == GPIO.LOW):
            reading += 1
        prin ("brightness   {}").format(reading)
        return reading
        '''
        return 100

    def button_1(self, BUT1PIN):
        GPIO.setup(BUT1PIN, GPIO.IN)
        if (GPIO.input(BUT1PIN) == False):
            print("button 1 was pushed")
        else:
            print (GPIO.input(BUT1PIN))

    def button_2(self, BUT2PIN):
        GPIO.setup(BUT2PIN, GPIO.IN)
        if (GPIO.input(BUT2PIN) == False):
            print("button 2 was pushed")

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

        if digits[i] == 'c':
            segment.writeDigitRaw(i, 99)
        elif digits[i] == 'h':
            segment.writeDigitRaw(i, 116)
        else:
            segment.writeDigit(i, int(digits[i]), dot)

def setBrightness(segment, currentBrightness):

    if currentBrightness < 50:
        segment.setBrightness(5)
    elif currentBrightness >= 50 and currentBrightness < 125:
        segment.setBrightness(10)
    else:
        segment.setBrightness(15)

def countdown(i):

    while(i!=-1):
        display(map(int, str(i).zfill(3)) )
        time.sleep(1)
        i-=1

def but1_callback(channel):
    print "button was pushed"

def LED(pin, status):
    GPIO.output(pin, status)


if __name__ == '__main__':

    #PIN VALUES
    DHTPIN = "25"
    BUT1PIN = 17
    BUT2PIN = 999
    BRIGHTPIN = 1
    OUTSIDEPIN = 24
    NEGATIVEPIN = 999
    OFFPIN = 22

    #Init the display
    segment = SevenSegment(address=0x70)
    segment.setBrightness(15)

    GPIO.setmode(GPIO.BCM)

    #Init buttons and set the callback
    GPIO.setup(BUT1PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUT1PIN, GPIO.FALLING, callback = but1_callback, bouncetime=300)

    #Init LEDs and shutdown switch
    GPIO.setup(OUTSIDEPIN, GPIO.OUT)
    #GPIO.setup(NEGATIVEPIN, GPIO.OUT)
    GPIO.setup(OFFPIN, GPIO.IN)

    #Ready the sensors
    sensor = SensorValues(DHTPIN, BRIGHTPIN, BUT1PIN, BUT2PIN)

    currentBrightness = 1
    wundergroundAPIKey = 'xxxxx'

    outsideWeather = weather.getWeather(wundergroundAPIKey)
    weatherTime = time.time()

    Loop = True
    while Loop:

        #Every 5 minutes update the outside weather conditions
        now = time.time()
        if (now - weatherTime) > 300:
            weatherTime = now
            outsideWeather = weather.getWeather(wundergroundAPIKey)

        insideTemp = str(sensor.getTemp())+'c'
        display(insideTemp , False)
        #if "-" in insideTemp :
        #    LED(NEGATIVEPIN, True)
        time.sleep(4)
        #LED(NEGATIVEPIN, False)

        outsideTemp = str(outsideWeather['tempC'])+'c'
        display(outsideTemp, False)
        LED(OUTSIDEPIN, True)
        #if "-" in outsideTemp:
        #    LED(NEGATIVEPIN, True)
        time.sleep(4)
        LED(OUTSIDEPIN, False)
        #LED(NEGATIVEPIN, False)

        display(str(sensor.getHum(DHTPIN))+'h', False)
        time.sleep(4)

        display(str(outsideWeather['humidity'])+'h', False)
        LED(OUTSIDEPIN, True)
        time.sleep(4)
        LED(OUTSIDEPIN, False)

        display(str(sensor.getPressure()), False)
        time.sleep(4)

        display(datetime.datetime.now(), True)
        time.sleep(6)

        #once a loop, check how bright it is, and adjust the display
        # THE HARDWARE IS NOT YET IMPLEMENTED
        currentBrightness = sensor.checkBrightness(BRIGHTPIN)
        setBrightness(segment, currentBrightness)

        #If switched is switched, shutdown the pi
        print GPIO.input(OFFPIN)
        if GPIO.input(OFFPIN):
            Loop = False

    segment.clear()
    GPIO.cleanup()
    #os.system("shutdown now")


