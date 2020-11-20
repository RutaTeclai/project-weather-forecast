"""CRUD operations."""

from model import db, User, Visit, Forecast_office, Forecast, connect_to_db
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



def create_visit(user, forecast_office):
    """ Create and return a new visit """

    visit = Visit(user=user, forecast_office=forecast_office)

    db.session.add(visit)
    db.session.commit()

    return visit


def create_forecast_office(forecast_office_id, office_name, grid_x, grid_y):
    """ Create and return a new Forecast Office - Wfo """

    forecast_office = Forecast_office(forecast_office_id=forecast_office_id, office_name=office_name,
                                        grid_x = grid_x, grid_y = grid_y)

    db.session.add(forecast_office)
    db.session.commit()

    return forecast_office


def create_forecast(temp_high, temp_low, image, weather_description, humidity, dew_point,
                    forecast_office_id,city, state,forecast_date=datetime.now()):
    
    """ Create adn return a new Forecast - weatherdata for a given date, default = now """

    forecast = Forecast(temp_high= temp_high, temp_low=temp_low, image=image, 
                        weather_description= weather_description, humidity=humidity,
                        dew_point= dew_point,forecast_office_id= forecast_office_id,
                        city=city, state=state,forecast_date= forecast_date)

    db.session.add(forecast)
    db.session.commit()

    return forecast


def get_user_by_email(email):
    
    user = User.query.filter(User.email == email).first()
    
    return user

def get_office_by_id(office_id):

    
    office = Forecast_office.query.filter(Forecast_office.forecast_office_id == office_id).first()
    
    return office


def get_visit_by_user_office(user_id, office_id):

    visit = Visit.query.filter(Visit.user_id == user_id and Visit.office_id).first()
    
    return visit

def get_visit_by_user(user_id):

    visit = Visit.query.filter(Visit.user_id == user_id).all()

    return visit

def get_user_by_id(user_id):

    user = User.query.filter(User.user_id == user_id).first()
    
    return user


if __name__ == '__main__':
    from server import app
    connect_to_db(app)