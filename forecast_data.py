""" """

from flask import (Flask, render_template, request, jsonify,
                    flash, session, redirect)
from datetime import datetime
from model import db, User, Visit, Forecast_office, Forecast, connect_to_db
import server
import crud

import requests
import json
import re  # for regual expression

periods= [
      {
        "number": 1,
        "name": "",
        "startTime": "2020-11-21T21:00:00-06:00",
        "endTime": "2020-11-21T22:00:00-06:00",
        "isDaytime": 'false',
        "temperature": 40,
        "temperatureUnit": "F",
        
        "windSpeed": "5 mph",
        "windDirection": "SE",
        "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
        "shortForecast": "Slight Chance Light Rain",
        "detailedForecast": ""
      },
      {
        "number": 2,
        "name": "",
        "startTime": "2020-11-21T22:00:00-06:00",
        "endTime": "2020-11-21T23:00:00-06:00",
        "isDaytime": 'false',
        "temperature": 39,
        "temperatureUnit": "F",
       
        "windSpeed": "0 mph",
        "windDirection": "S",
        "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
        "shortForecast": "Slight Chance Light Rain",
        "detailedForecast": ""
      },
      {
        "number": 3,
        "name": "",
        "startTime": "2020-11-21T23:00:00-06:00",
        "endTime": "2020-11-22T00:00:00-06:00",
        "isDaytime": 'false',
        "temperature": 39,
        "temperatureUnit": "F",
        
        "windSpeed": "0 mph",
        "windDirection": "W",
        "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
        "shortForecast": "Patchy Fog",
        "detailedForecast": ""
      },
      {
        "number": 4,
        "name": "",
        "startTime": "2020-11-22T00:00:00-06:00",
        "endTime": "2020-11-22T01:00:00-06:00",
        "isDaytime": 'false',
        "temperature": 38,
        "temperatureUnit": "F",
        
        "windSpeed": "0 mph",
        "windDirection": "NW",
        "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
        "shortForecast": "Patchy Fog",
        "detailedForecast": ""
      },]



def lat_lng_city_state(city_name,state):

    city_data = open('data/cities_geodata.json').read()

    city_data_dict = json.loads(city_data)
    latitude = ''
    longitude = ''
    for city in city_data_dict:
        
         if city['city'] == city_name and city['state_id'] == state:
            latitude = city['lat']
            longitude = city['lng']
            

    return f'{latitude},{longitude}'


def get_gridpoints(points):

    res = requests.get(f'https://api.weather.gov/points/{points}')
    grid = res.json()

    gridpoints = {'grid_id': grid['properties']['gridId'], 
                    'grid_x': grid['properties']['gridX'],
                    'grid_y': grid['properties']['gridY'],
                    'forecast_hourly': grid['properties']['forecastHourly'],
                    'forecast': grid['properties']['forecast']
                }

    return gridpoints


def show_forecast(forcast_url):

    res = requests.get(f'{forcast_url}')
    # requests.get(f'https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast')

    forecast = res.json()

    return forecast


def get_office_name(office_id):

    res = requests.get(f'https://api.weather.gov/offices/{office_id}')
    office_name = res.json()['name']

    return office_name


def iso_to_date(date_iso_format):

    match_obj = re.search(r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$', date_iso_format)

    date_time = datetime.strptime(f'{match_obj.group(1)}-{match_obj.group(2)}-{match_obj.group(3)}{match_obj.group(4)}:{match_obj.group(5)}:{match_obj.group(6)}', '%Y-%m-%d%H:%M:%S')

    return date_time


def reg_date(date_value):
    # updated= "2020-11-20T20:11:40+00:00"

    match_obj = re.search(r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$', date_value)

    date_time = datetime.strptime(f'{match_obj.group(1)}-{match_obj.group(2)}-{match_obj.group(3)}{match_obj.group(4)}:{match_obj.group(5)}:{match_obj.group(6)}', '%Y-%m-%d%H:%M:%S')

    
    
   
    
    # match_obj.group()        this prints out the whole string or the string you are matching with the regexp
    # 2020-11-20T20:11:40+00:00
    # match_obj.group(1)        ---- 2020
    # match_obj.group(2)          ----- 11

    # match_obj.group(1)
    # match_obj.group(2)
    # match_obj.group(3)

    
    print(f'D - {date_time}')
    print(f'the date --- {date_time.date()}')
    # print(date_time.time())
    print(date_time.time().strftime("%-I %p"))
    # print(time.strftime("%-I %p"))
    

    # print(datetime.now().date())

    # datetime.strptime changes the result from the regExp to date with the given format
    
    
    # date = datetime.strptime(f'{match_obj.group(1)}-{match_obj.group(2)}-{match_obj.group(3)}', '%Y-%m-%d').date()
   
    # .date() returns only date part 
    # return date
    

    

def hourly_forecast():

    date_str = iso_to_date(periods[0]['startTime'])

    data = []
    
    for period in periods:

        if (iso_to_date(period['startTime'])).date() == date_str.date():

            # time = (iso_to_date(period['startTime'])).time().strftime("%-I %p")
            time = period['startTime']
            temp = period['temperature']
            data.append({'time':f'{time}', 'temp':temp })
           
            print(period['temperature'])
            
            print((iso_to_date(period['startTime'])).time().strftime("%-I %p"))

    hourly_forecast = {'forecasts':data}

    return hourly_forecast





    
    


def list_value():

    lst = [1,2,3,4,5,5,5,3,4]
    
    for num in lst:

        if num == 5:
            print(num)

