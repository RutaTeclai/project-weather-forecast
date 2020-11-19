"""Server for weather forecasts app."""

from flask import (Flask, render_template, request,
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

    state_code_dict= get_state_code()

    return render_template('homepage.html', state_code = state_code_dict)


@app.route('/login')
def show_method():
    
    email= request.args.get('email')
    password= request.args.get('password')

    user= crud.get_user_by_email(email)
   

    if user and user.password == password:
        city = user.city
        state = user.state

        print(f'{city} {state}')
        state_code_dict= get_state_code()

        points = forecast_data.lat_lng_city_state(city,state)
        grid = forecast_data.get_gridpoints(points)
        forecast_url = grid['forecast']
        forecast_dict = forecast_data.show_forecast(forecast_url)
        return render_template('forecastpage.html', forecast = forecast_dict, state_code = state_code_dict, city=city, state=state)

    else:
        flash("Enter correct email and password or create a new user account")
        return redirect('/')

    return "forecast"


@app.route('/forecast_search')
def show_request():

    city = request.args.get('city')
    state = request.args.get('state')

    points = forecast_data.lat_lng_city_state(city,state)

    state_code_dict= get_state_code()
    if points == ",":

        flash("Enter correct city and state combination")
        return render_template('forecastpagecopy.html', state_code = state_code_dict)

    else:

        grid = forecast_data.get_gridpoints(points)
        forecast_url = grid['forecast']
        forecast_dict = forecast_data.show_forecast(forecast_url)

        forecast_office = crud.get_office_by_id(grid['grid_id'])
        if not forecast_office:
            forecast_office_id = grid['grid_id']
            office_name = forecast_data.get_office_name(forecast_office_id)
            grid_x = grid['grid_x']
            grid_y = grid['grid_y']

            crud.create_forecast_office(forecast_office_id, office_name, grid_x, grid_y)

        


        return render_template('forecastpage.html', forecast = forecast_dict, state_code = state_code_dict, city=city, state=state)
        



    


def get_state_code():

    state_code = open('data/data.json').read()
    state_code_dict = json.loads(state_code)

    return state_code_dict







if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)