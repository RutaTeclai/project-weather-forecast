"""Server for weather forecasts app."""

from flask import (Flask, render_template, request,
                    flash, session, redirect)
from model import connect_to_db
import crud
import forecast_data
from jinja2 import StrictUndefined

import json
import requests



def get_state_code():

    state_code = open('data/data.json').read()
    state_code_dict = json.loads(state_code)

    return state_code_dict

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)