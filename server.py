"""Server for weather forecasts app."""

from flask import (Flask, render_template, request,jsonify,
                    flash, session, redirect)
from model import connect_to_db
import crud
import forecast_data
from jinja2 import StrictUndefined

import json

import requests


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """ show homepage --- log-in form & button (create user)"""
    state_code_dict= get_state_code()

    return render_template('homepage.html', state_code = state_code_dict)



    
@app.route('/create_user', methods=['POST'])
def user():

    fname= request.form.get('fname')
    lname= request.form.get('lname')
    email= request.form.get('email')
    password= request.form.get('password')
    city= request.form.get('city')
    state= request.form.get('state')

    user = crud.get_user_by_email(email)

    if user:
        """ user_account already exists or the email already in use """
        return "1"
        
    else:
        """ no user_account exists and create a user account """
        user = crud.create_user(fname, lname, email, password, city, state)
        # forecast_office = crud.jcity,state)
        # if not forecast_office:
        #     data = forecast_data.api_data(city,state)
        #     add_data_todb(data)

    return "2"


@app.route('/login')
def show_method():
    
    email= request.args.get('email')
    password= request.args.get('password')

    user= crud.get_user_by_email(email)
   

    if user and user.password == password:

        city = user.city
        state = user.state

        session['user'] = user.user_id

        state_code_dict= get_state_code()

        grid,forecast_dict, office_name, office_id, hourly_forecast, station_dict, station_forecast = (forecast_tuple(city,state))

        return render_template('forecastpage.html',forecast = forecast_dict,
                                state_code = state_code_dict,
                                city=city, state=state,
                                office_name = office_name,
                                forecast_id = office_id,
                                hourly_forecast= hourly_forecast,
                                station_dict = station_dict,
                                station_forecast = station_forecast)


    else:
        flash("Enter correct email and password or create a new user account")
        return redirect('/')


@app.route('/forecast_search')
def show_request():

    city = request.args.get('city')
    state = request.args.get('state')

    user_id = session.get('user')

    state_code_dict= get_state_code()

    points = forecast_data.lat_lng_city_state(city,state)
    if points:

        grid,forecast_dict, office_name, office_id, hourly_forecast, station_dict, station_forecast= (forecast_tuple(city,state))
        # print(grid)
        grid_x= grid['grid_x']
        grid_y = grid['grid_y']
        endpoint = grid['office_endpoint']

        forecast_office = crud.get_office_by_id(office_id)
        if not forecast_office:

            forecast_office = crud.create_forecast_office(office_id, office_name, grid_x, grid_y,endpoint)

        crud.create_visit(user_id,office_id)

        return render_template('forecastpage.html',forecast = forecast_dict,
                                state_code = state_code_dict,
                                city=city, state=state,
                                office_name = office_name,
                                forecast_id = office_id,
                                hourly_forecast= hourly_forecast,
                                station_dict = station_dict,
                                station_forecast = station_forecast)

    else:
        flash("Enter valid City and State combination")
        return render_template('forecastpagecopy.html', state_code = state_code_dict)


@app.route('/news')
def get_news():
    
    office_id = request.args.get('id')
    
    articles = forecast_data.get_news_headlines(office_id)

    return jsonify(articles)

    

def articles_dict(articles):

    articles_dict = {}
    lst = []
    for article in articles:

        print(article['title'])

@app.route('/hourly-forecast')  # TODo after doing all the things in forecast_data
def show_hourly_forecast():

    hourly_forecast_= forecast_data.get_hourly_forecast

    # data = forecast_data.hourly_forecast()

    # return jsonify(tbl)

def get_state_code():

    state_code = open('data/data.json').read()
    state_code_dict = json.loads(state_code)

    return state_code_dict


def add_data_todb(data):   # takes the return value of the api_data

    grid, office_name, station, city, state = data

    
    grid_id, grid_x, grid_y, endpoint = (grid['grid_id'],grid['grid_x'],grid['grid_y'],grid['office_endpoint'])
    station_id, station_name, elev, obs_url = (station['station_id'],station['station_name'],station['elevation'],station['observation'])


    crud.create_forecast_office(grid_id, office_name, grid_x, grid_y,endpoint)
    crud.create_station(station_id, station_name,elev, grid_id,obs_url)
    crud.create_city(city,state,grid_id)

def forecast_tuple(city,state):

    grid, office_name,station = forecast_data.api_data(city,state)
    office_id = grid['grid_id']


    endpt = grid['office_endpoint']
    obs_url = station['observation']

    forecast_url = f'{endpt}/forecast'
    hourly_forecast = f'{forecast_url}/hourly'
    forecast_dict = forecast_data.show_forecast(forecast_url)
    station_dict = station
    station_forecast = forecast_data.station_forecast(obs_url)
    return (grid,forecast_dict,office_name,office_id,hourly_forecast, station_dict,station_forecast)




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)