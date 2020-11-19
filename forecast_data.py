""" """

from flask import (Flask, render_template, request,
                    flash, session, redirect)
from model import db, User, Visit, Forecast_office, Forecast, connect_to_db
import server
import crud

import requests
import json


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



