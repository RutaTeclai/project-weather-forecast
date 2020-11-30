"""CRUD operations."""

from model import db, User, Visit, Forecast_office, Forecast,Station, City, connect_to_db
import server
# from model import db, User, Visit, Forecast_office, Station, Geodata, Forecast, connect_to_db
from datetime import datetime

def create_user(fname, lname, email, password, city, state):
    """Create and return a new user."""

    user = User(fname=fname,lname=lname,
                email=email, password=password,
                city=city, state=state)

    db.session.add(user)
    db.session.commit()

    return user

def create_city(city,state,forecast_office_id):
    """ Create and return a new city"""

    city = City(city=city,state=state,forecast_office_id=forecast_office_id)

    db.session.add(city)
    db.session.commit()

    return city

def create_visit(user_id, forecast_office_id):
    """ Create and return a new visit """

    visit = Visit(user_id=user_id, forecast_office_id=forecast_office_id)

    db.session.add(visit)
    db.session.commit()

    return visit


def create_forecast_office(forecast_office_id, office_name, grid_x, grid_y,endpoint):
    """ Create and return a new Forecast Office - Wfo """

    forecast_office = Forecast_office(forecast_office_id=forecast_office_id, office_name=office_name,
                                        grid_x = grid_x, grid_y = grid_y, office_endpoint = endpoint)

    db.session.add(forecast_office)
    db.session.commit()

    return forecast_office, 


def create_forecast(temp_high, temp_low, image, weather_description, humidity, dew_point,
                    forecast_office_id,city, state,forecast_date=datetime.now()):
    
    """ Create and return a new Forecast - weatherdata for a given date, default = now """

    forecast = Forecast(temp_high= temp_high, temp_low=temp_low, image=image, 
                        weather_description= weather_description, humidity=humidity,
                        dew_point= dew_point,forecast_office_id= forecast_office_id,
                        city=city, state=state,forecast_date= forecast_date)

    db.session.add(forecast)
    db.session.commit()

    return forecast


def create_station(station_id, station_name,elevation, forecast_office_id,obs_url):
    """ Create and return a new Forecast Observation Station aka Station """

    station = Station(station_id = station_id, station_name = station_name,
                        elevation = elevation, forecast_office_id = forecast_office_id,
                        observation_url = obs_url)

    db.session.add(station)
    db.session.commit()

    return station

def get_user_by_email(email):
    
    """ return a user (obj) for the given email """
    user = User.query.filter(User.email == email).first()
    
    return user

def get_office_by_id(office_id):
    """ return forecast_office (obj) for the given forecast_office_id"""

    office = Forecast_office.query.filter(Forecast_office.forecast_office_id == office_id).first()
    return office

def get_station_by_office(office_id):
    """ return a station (obj) for the given forecast_office_id --- a fk in station"""

    station = Station.query.filter(Station.forecast_office_id == office_id).first()
    return station

def get_visit_by_user_office(user_id, office_id):
    """ return a visit (obj) for the given user_id and office_id"""

    visit = Visit.query.filter(Visit.user_id == user_id, Visit.forecast_office_id == office_id).first()
    
    return visit


def get_visit_by_user(user_id):
    """ return visit (obj) --- all visits by a user with user_id"""

    visit = Visit.query.filter(Visit.user_id == user_id).all()

    return visit


def get_user_by_id(user_id):
    """ return user obj for the given user_id --- all info about a user"""

    user = User.query.filter(User.user_id == user_id).first()
    
    return user

def get_city_by_name(city,state):
    """ return a city (obj) for the given city name & state --- """

    city = City.query.filter(City.city == city, City.state == state).first()

    return city


def get_office_by_city(city,state):
    """ return forecast_office (obj) from the City Class"""
    city = City.query.filter(City.city == city, City.state == state).first()

    return city.forecast_office 


def get_city_by_office(office_id):
    city = City.query.filter(City.forecast_office_id == office_id).first()
    return city

if __name__ == '__main__':
    from server import app
    connect_to_db(app)