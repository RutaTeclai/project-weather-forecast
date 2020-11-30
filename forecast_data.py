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

api = 'https://api.weather.gov/'  # url for NWS API -- global variable used to make requests from the API

# periods= [
#       {
#         "number": 1,
#         "name": "",
#         "startTime": "2020-11-21T21:00:00-06:00",
#         "endTime": "2020-11-21T22:00:00-06:00",
#         "isDaytime": 'false',
#         "temperature": 40,
#         "temperatureUnit": "F",
        
#         "windSpeed": "5 mph",
#         "windDirection": "SE",
#         "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
#         "shortForecast": "Slight Chance Light Rain",
#         "detailedForecast": ""
#       },
#       {
#         "number": 2,
#         "name": "",
#         "startTime": "2020-11-21T22:00:00-06:00",
#         "endTime": "2020-11-21T23:00:00-06:00",
#         "isDaytime": 'false',
#         "temperature": 39,
#         "temperatureUnit": "F",
       
#         "windSpeed": "0 mph",
#         "windDirection": "S",
#         "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
#         "shortForecast": "Slight Chance Light Rain",
#         "detailedForecast": ""
#       },
#       {
#         "number": 3,
#         "name": "",
#         "startTime": "2020-11-21T23:00:00-06:00",
#         "endTime": "2020-11-22T00:00:00-06:00",
#         "isDaytime": 'false',
#         "temperature": 39,
#         "temperatureUnit": "F",
        
#         "windSpeed": "0 mph",
#         "windDirection": "W",
#         "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
#         "shortForecast": "Patchy Fog",
#         "detailedForecast": ""
#       },
#       {
#         "number": 4,
#         "name": "",
#         "startTime": "2020-11-22T00:00:00-06:00",
#         "endTime": "2020-11-22T01:00:00-06:00",
#         "isDaytime": 'false',
#         "temperature": 38,
#         "temperatureUnit": "F",
        
#         "windSpeed": "0 mph",
#         "windDirection": "NW",
#         "icon": "https://api.weather.gov/icons/land/night/rain,20?size=small",
#         "shortForecast": "Patchy Fog",
#         "detailedForecast": ""
#       }]



def lat_lng_city_state(city_name,state):
    """ return latitude,longitude for a given city_name and state (valid combination) 
    from cities_geodata.json ---- return None if the city_name, state combination not in the Json file"""

    city_data = open('data/cities_geodata.json').read()

    city_data_dict = json.loads(city_data)
    
    for city in city_data_dict:
        
        if city['city'] == city_name and city['state_id'] == state:
            latitude = city['lat']
            longitude = city['lng']
            return f'{latitude},{longitude}'

        
def get_gridpoints(point):
    """ return forecast office data - gridId, gridX, gridY for a given point --- (lat,lng)  """

    # request the National Weather Service (NWS) API - endpoint --> points
    res = requests.get(f'{api}points/{point}')

    if res.status_code == 200:
        
        grid = res.json()

        gridpoints = {'grid_id': grid['properties']['gridId'], 
                        'grid_x': grid['properties']['gridX'],
                        'grid_y': grid['properties']['gridY'],
                        'office_endpoint':grid['properties']['forecastGridData']
                        # 'forecast_hourly': grid['properties']['forecastHourly'],
                        # 'forecast': grid['properties']['forecast']
                    }

        return gridpoints


def get_office_name(office_id):

    res = requests.get(f'{api}/offices/{office_id}')
    office_name = res.json()['name']

    return office_name


def get_station_name(grid_points):

    res = requests.get(f'{api}gridpoints/{grid_points}/stations')
    station_info = res.json()['features'][0]['properties']
    station_id = station_info['stationIdentifier']
    station_dict = {
        'station_id': station_id,
        'station_name': station_info['name'],
        'elevation': station_info['elevation']['value'],
        'observation': f'{api}stations/{station_id}/observations/latest?require_qc=true'
        
    }

    return station_dict

def station_forecast(observation_url):

    res = requests.get(observation_url)
    stn_forecast = res.json()
    temp = (stn_forecast['properties']['temperature']['value'] * 1.8) + 32
    dewpoint = (stn_forecast['properties']['dewpoint']['value'] * 1.8) + 32
    humidity = stn_forecast['properties']['relativeHumidity']['value']
    
    # windSpeed = stn_forecast['properties']['windSpeed']['value']  --- it returns none
    
    # windSpeed = (stn_forecast['properties']['windSpeed']['value'] * 0.621)
    # windDirection & windSpeed --- get it from the detailed forecast
    visibility = (stn_forecast['properties']['visibility']['value'] * 0.0006)

    
    stn_dict = {
        'temp': temp,
        'dewpoint': round(dewpoint),
        'humidity': round(humidity),
        # 'windspeed': round(windSpeed),
        # # 'windspeed': windSpeed,
        'visibility': round(visibility)
    }

    return  stn_dict


def show_forecast(forcast_url):

    res = requests.get(forcast_url)
    # requests.get(f'https://api.weather.gov/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast')

    forecast = res.json()

    return forecast

def get_news_headlines(office_id):

    newspaper = {}
    url = f'{api}offices/{office_id}/headlines'
    
    res = requests.get(url)
    articles = res.json()['@graph']
    newspaper['articles'] = articles
    return newspaper

def get_hourly_forecast(hourly_forecast_url):

    res = requests.get(hourly_forecast_url)
    hourly_forecast = res.json()

    return hourly_forecast['periods']

# def iso_to_date(date_iso_format):

#     match_obj = re.search(r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$', date_iso_format)

#     date_time = datetime.strptime(f'{match_obj.group(1)}-{match_obj.group(2)}-{match_obj.group(3)}{match_obj.group(4)}:{match_obj.group(5)}:{match_obj.group(6)}', '%Y-%m-%d%H:%M:%S')

#     return date_time


# def reg_date(date_value):
#     # updated= "2020-11-20T20:11:40+00:00"

#     match_obj = re.search(r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$', date_value)

#     date_time = datetime.strptime(f'{match_obj.group(1)}-{match_obj.group(2)}-{match_obj.group(3)}{match_obj.group(4)}:{match_obj.group(5)}:{match_obj.group(6)}', '%Y-%m-%d%H:%M:%S')

    
    
   
    
#     # match_obj.group()        this prints out the whole string or the string you are matching with the regexp
#     # 2020-11-20T20:11:40+00:00
#     # match_obj.group(1)        ---- 2020
#     # match_obj.group(2)          ----- 11

#     # match_obj.group(1)
#     # match_obj.group(2)
#     # match_obj.group(3)

    
#     print(f'D - {date_time}')
#     print(f'the date --- {date_time.date()}')
#     # print(date_time.time())
#     print(date_time.time().strftime("%-I %p"))
#     # print(time.strftime("%-I %p"))
    

#     # print(datetime.now().date())

#     # datetime.strptime changes the result from the regExp to date with the given format
    
    
#     # date = datetime.strptime(f'{match_obj.group(1)}-{match_obj.group(2)}-{match_obj.group(3)}', '%Y-%m-%d').date()
   
#     # .date() returns only date part 
#     # return date
    

    

# def hourly_forecast():

#     date_str = iso_to_date(periods[0]['startTime'])

#     data = []
    
#     for period in periods:

#         if (iso_to_date(period['startTime'])).date() == date_str.date():

#             # time = (iso_to_date(period['startTime'])).time().strftime("%-I %p")
#             time = period['startTime']
#             temp = period['temperature']
#             data.append({'time':f'{time}', 'temp':temp })
           
#             print(period['temperature'])
            
#             print((iso_to_date(period['startTime'])).time().strftime("%-I %p"))

#     hourly_forecast = {'forecasts':data}

#     return hourly_forecast





    
def pas(x,y):
    return  x+y

def show():
    
    pas(2,3)
    print('not used return value')

def use():
    val = pas(2,3)
    print('return value used')

# def list_value():

#     lst = [1,2,3,4,5,5,5,3,4]
    
#     for num in lst:

#         if num == 5:
#             print(num)


def api_data(city,state):

    points = lat_lng_city_state(city,state)
    grid = get_gridpoints(points)
    grid_id, grid_x,grid_y = (grid['grid_id'],grid['grid_x'],grid['grid_y'])
    office_name = get_office_name(grid_id)
    station = get_station_name(f"{grid_id}/{grid_x},{grid_y}")

    return (grid, office_name,station)
    # (grid, office_name,station,city,state)
    
