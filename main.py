import threading

# import "packages" from flask
from flask import render_template  # import render_template from "public" flask libraries

# import "packages" from "this" project
from __init__ import app,db  # Definitions initialization
from model.jokes import initJokes
from model.users import initSongs, initUsers
from model.players import initPlayers


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
from api.song import song_api


# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


""" 
JWT test
""" 

from flask import jsonify, request, make_response, redirect, session
import jwt 
import datetime 
from functools import wraps
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies)
from flask_session import Session 
import os
#from __init__ import ApplicationConfig

""" 
"""


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(song_api) 


""" 
JWT test
""" 


app.config['SECRET_KEY'] = 'secretkey'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

jwt = JWTManager(app)


""" 
""" 



@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")



@app.route('/testing')
def testing():
    access_token = create_access_token(identity=str("usertest"))
    refresh_token = create_refresh_token(identity=str("usertest"))
    resp = make_response(redirect("http://swifties.duckdns.org/", 302))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return jsonify( {
        "id": access_token
    })



@app.before_first_request
def activate_job():  # activate these items 
    initJokes()
    initUsers()
    #initSongs()
    initPlayers()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app)
    #initSongs()
    app.run(debug=True, host="0.0.0.0", port="8086")
