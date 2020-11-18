""" Models for weather forecasts app. """


from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(30), nullable = False)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)

    visit = db.relationship('Visit')
   

    def __repr__(self):
        """ show info about user """
        return f'<User user_id={self.user_id} email={self.email} city={self.city}, state={self.state}>'


class Visit(db.Model):
    """ A Forecast office Visit """

    __tablename__ = 'visits'

    visit_id = db.Column(db.Integer, 
                autoincrement=True,
                primary_key= True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    forecast_office_id = db.Column(db.String, db.ForeignKey('forecast_offices.forecast_office_id'))

    user = db.relationship('User')
    forecast_office = db.relationship('Forecast_office')


    def __repr__(self):
        """ show info about visit """
        return f'<Visit user_id={self.user_id}, forecast_office_id {self.forecast_office_id}>'



class Forecast_office(db.Model):
    """ A Weather Forecast office - Wfo """

    __tablename__ = 'forecast_offices'

    forecast_office_id = db.Column(db.String, 
                                     primary_key= True)
    office_name = db.Column(db.String, nullable = False, unique = True)
    grid_x = db.Column(db.Integer, nullable= False)
    grid_y= db.Column(db.Integer, nullable= False)


    visit = db.relationship('Visit')
    # station = db.relationship('Station')
    forecast = db.relationship('Forecast')


    def __repr__(self):
        """ show info about Weather Forecast office  """
        return f'<Forecast Office forecast_office_id={self.forecast_office_id} Forecast Office={self.office_name}>'


class Forecast(db.Model):
    """ A forecast info  """

    __tablename__ = 'forecasts'

    forecast_id = db.Column(db.Integer, autoincrement = True,
                            primary_key = True)
    forecast_office_id = db.Column(db.String, db.ForeignKey('forecast_offices.forecast_office_id'))
    temp_high = db.Column(db.Float, nullable=False, 
                    unique = True)
    temp_low = db.Column(db.Float, nullable = False)
    image = db.Column(db.String, nullable = False)
    weather_description = db.Column(db.String, nullable = False)
    humidity = db.Column(db.Float)
    dew_point = db.Column(db.Float)
    forecast_date= db.Column(db.DateTime)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    
    forecast_office = db.relationship('Forecast_office')

    def __repr__(self):
        """ show info about Forecast """
        return f'<Forecast Temp_high={self.temp_high} Temp_low= {self.temp_low} forecast_date= {self.forecast_date}, humidity= {self.humidity}>'




def connect_to_db(flask_app, db_uri='postgresql:///forecasts', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)
    
    
    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
