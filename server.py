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

newspaper = {'articles':[
                            {"link": "https://www.surveymonkey.com/r/frostfreeze","title": "We need your opinions!  Please take our Frost / Freeze product public survey open until 12/17/20"},
                            {"link": "https://www.weather.gov/media/top/newsletter/Fall 2020 Topeka Tiller.pdf","title": "Fall 2020 NWS Topeka Newsletter"},
                            {"link": "https://www.google.com", 'title': "Search Engine"}
                        ]
   }



@app.route('/')
def homepage():

    state_code_dict= get_state_code()

    return render_template('homepage.html', state_code = state_code_dict)
    # return render_template('ajax.html')

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
        crud.create_user(fname, lname, email, password, city, state)
        return "2"
        




# @app.route('/create_user', methods=['POST'])
# def create_user_account():
#     """ Register a new User """

#     fname= request.form.get('fname')
#     lname= request.form.get('lname')
#     email= request.form.get('email')
#     password= request.form.get('password')
#     city= request.form.get('city')
#     state= request.form.get('state')

#     user = crud.get_user_by_email(email)
   

#     if user:
#         flash("The email already in use. Use different email!")
        

#     else:
#         crud.create_user(fname, lname, email, password, city, state)
#         flash("Account successful created. Please Log In")

#     return redirect('/')




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

        points = forecast_data.lat_lng_city_state(city,state)
        grid = forecast_data.get_gridpoints(points)
        forecast_url = grid['forecast']
        forecast_id = grid['grid_id']
        # forecast_id = grid
        office_name = forecast_data.get_office_name(forecast_id)
        forecast_dict = forecast_data.show_forecast(forecast_url)
        
        return render_template('forecastpage.html', forecast = forecast_dict, 
                                state_code = state_code_dict, city=city, state=state,
                                office_name = office_name,
                                forecast_id = forecast_id,
                                grid = grid['forecast_hourly'])

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
        forecast_office_id = grid['grid_id']
        office_name = forecast_data.get_office_name(forecast_office_id)
        grid_x = grid['grid_x']
        grid_y = grid['grid_y']
        if not forecast_office:
            

            crud.create_forecast_office(forecast_office_id, office_name, grid_x, grid_y)

        user_id = session.get('user')

        visit = get_visit_by_user_office(user_id,forecast_office_id)

        if not visit:
            user = crud.get_user_by_id(user_id)
            crud.create_visit(user,forecast_office)

            

    
    return render_template('forecastpage.html', forecast = forecast_dict, state_code = state_code_dict, 
                            city=city, state=state,office_name = office_name,
                            forecast_id = forecast_office_id,
                            grid = grid['forecast_hourly'])
        
 
@app.route('/hourly-forecast/<grid>')
def get_hourly_forecast():

    forecast_link = grid['forecast_hourly']
    print(f' the forecast link --- {forecast_link}')
    return forecast_link




@app.route('/offices')
def show_offices(): 

    # after session works get all offices visited by user

    visits = crud.get_visit_by_user(2)
    for visit in visits:

        offices = visit.forecast_office_id

        print(offices)
    return "offices"

# @app.route("/ajax-view")
# def get_ele():

#     return "working"

# @app.route('/news', methods=['POST'])   
# def show_news():

#     office_id = request.form.get('office-id')
#     res = request.get(f'https://api.weather.gov/offices/{ office_id}/headlines')


def get_state_code():

    state_code = open('data/data.json').read()
    state_code_dict = json.loads(state_code)

    return state_code_dict


@app.route('/news')
def get_news():

    office_id = request.args.get('id')
    print(office_id)

    return jsonify(newspaper)

@app.route('/hourly-forecast')
def show_hourly_forecast():

    tbl = forecast_data.hourly_forecast()

    return jsonify(tbl)
    




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)