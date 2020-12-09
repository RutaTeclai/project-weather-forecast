# Hackbright Academy Capstone Project

## Weather Forecast (*ShowMeForecast*)

### Project Description ###
_Weather Forecast is a full stack web app that allows users to see 6 days Weather Forecast for any location by searching by city._
_The forecast page has detailed information about Weather Forecast Office, Observation Station and its weather condition. It uses the National Weather Service (NWS) API._

### Technologies Used
* Python
* Flask
* Jinja
* JavaScript
* jQuery
* Ajax
* html
* CSS
* PostgreSQL
* SQLAlchemy

### MVP
* Users can see Forecast of any City/Location
* Users can see hourly Forecast
* Users can go to the Forecast office Website and read News Headlines from the Forecast Office

#### 2.0
* Users can register and Sign-in

### Future Implementations
* implement autocomplete for user entery of City,State
* get an API for Weather record to trend the climate change
* get Weather alerts and notify users

__You can run the app locally__

1. Requirements
* Python3.x.x
* Postgresql

2. clone the project repo -- [https://github.com/RutaTeclai/Weather-Forecast.git]

3. install virtual environment and activate it
* $ virtualenv env --always--copy     **--always--copy** for windows users
* $ source env/bin/activate

4. install Flask & other dependencies
* $ pip3 install -r requirements.txt

5. create __forecasts__ psql database and all its tables
* $ createdb forecasts
* run model.py in interactive mode   **$ python3 -i model.py**
* >>> db.create_all()

6. run the server 
* $ python3 server.py

7. open any browser and **localhost:5000**







