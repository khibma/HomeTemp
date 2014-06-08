
import urllib
import json


def getCurrentConditions(apiKey):

    cityURL = "http://api.wunderground.com/api/{}/geolookup/conditions/q/Canada/Ottawa.json".format(apiKey)

    cityResponse = urllib.urlopen(cityURL)
    jCityResponse = json.loads(cityResponse.read())
    tempC = jCityResponse['current_observation']
    return tempC

def getWeather(apiKey):

    wJSON = getCurrentConditions(apiKey)

    return {"tempC": wJSON['temp_c'],
            "humidity" : wJSON['relative_humidity'],
            "feesLikeC" : wJSON['feelslike_c'] }