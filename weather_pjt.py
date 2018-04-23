# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 23:16:08 2018

@author: Chat
"""

import pip

def install():
    pip.main(['install', 'beautifulsoup4'])
    pip.main(['install', 'weather-api'])
    pip.main(['install', 'urllib3'])


import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from weather import Weather, Unit
import superSecret as s
import send_email_file




def fetch_weather(your_location):
    global date, condition, now
    now = datetime.datetime.now()
    date = [now.month, now.day, now.year]
    weather = Weather(unit=Unit.FAHRENHEIT)
    location = weather.lookup_by_location(your_location)
    forecasts = location.forecast()#
    i = []
    for x in forecasts:
        i.append(vars(x))
    #Fetches Todays Wether then stores the high and low in a dictionary with the date as the key
    todays_forecast = {}
    todays_forecast[i[0]['_forecast_data']['date']] = [i[0]['_forecast_data']['high'], i[0]['_forecast_data']['low']]
    return todays_forecast


def shorts():
    web_page = 'http://caniwearshorts.today/?location=Auburn%2C+AL'
    page = urlopen(web_page)
    soup = BeautifulSoup(page, 'html.parser')
    shorts_span = soup.find('h1', attrs={'style': 'font-size: 70px'})
    shorts = shorts_span.text
    return shorts

def compose(carrier, phone, your_location):
    if carrier == "Verizon":
        to = phone + "@vtext.com"
    elif carrier == "Sprint":
        to = phone + "@messaging.sprintpcs.com"
    elif carrier == "AT&T":
        to = phone + "@txt.att.net"
    elif carrier == "T-Mobile":
        to = phone + "@tmomail.net"
    else:
        return("Invalid Carrier!!!")
    todays_weather = fetch_weather(your_location)#
    msg = message(date_str, todays_weather, your_location, key_date)
    mail = send_email_file.sendemail(s.username, to, "", "Good Morning - Weather Bot", msg, s.username, s.password)
    return mail
   

def message(date_str, todays_weather, your_location, key_date):
    message = date_str + "\r\r" + conditionText(your_location) + "\r\r" + "Should I wear shorts?: " + str(shorts()) + "\r" + "Low: " + str(todays_weather[key_date][1]) + "\r" + "High: " + str(todays_weather[key_date][0])
    return(message)

def conditionText(your_location):
    weather = Weather(unit=Unit.FAHRENHEIT)
    location = weather.lookup_by_location(your_location)
    condition = location.condition()
    if condition.text() == "Scattered Thunderstorms":
        condition_text = "It might be a good idea to bring an umbrella if you're going out."
    elif condition.text() == "Thunderstorms":
        condition_text = "You should definatly bring an umbrella out with you today."
    elif condition.text() == "Sunny":
        condition_text = "No rain for today! Enjoy the Sun."
    elif condition.text() == 'Mostly Cloudy':
        condition_text = "There will be dark skys but no rain in the forecast!"
    elif condition.text() == 'Breezy':
        condition_text = "There will be lots of wind. Don't get blown over!"
    elif condition.text() == 'Clear':
        condition_text = "Its clear out today!"
    else:
        condition_text = condition.text()
    return condition_text

now = datetime.datetime.now()
date = [now.month, now.day, now.year]
date_str = str(date[0]) +"/"+ str(date[1]) +"/"+ str(date[2])
key_date = str(date[1]) + " " + now.strftime("%b") + " " + str(date[2])
