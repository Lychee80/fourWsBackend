import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User


from __init__ import app,db  # Definitions initialization
#db.init_app(app)

from flask import jsonify, request, make_response
import jwt 
# import datetime 
from functools import wraps

from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, decode_token)

from werkzeug.security import generate_password_hash, check_password_hash

""" 
recommender 
"""
from recommender2 import ImplicitRecommender
from data2 import loadCountrySong, SongRetriever
import implicit
import scipy


from flask_cors import CORS
CORS(app)

app.config['SECRET_KEY'] = 'secretkey'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

jwt = JWTManager(app)


user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)



class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 1:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            dob = body.get('dob')

            country = body.get('country')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
            uo.country = country
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')
            
            ''' Find user '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None or not user.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user '''
            return jsonify(user.read())

    class _Login(Resource): # This is currently broken; accepts any set of login credentials. Authentication function is in progress
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            username = body.get('username')
            password = body.get('password')
            
            
            dbUser = User.query.filter_by(_uid=username).first()

            
            if dbUser is None:
                return {'message': f"Invalid user id"}, 400

            
            dbUsername = dbUser.uid
            dbPassword = dbUser.password

            if not check_password_hash(dbPassword, password):
                return {'message': f"Invalid password"}, 400
            



            access_token = create_access_token(identity=str(username))

            return jsonify( {
                "id": access_token
            })

    class _Info(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            token = body.get('token')
            
            decoded = decode_token(token)

            return jsonify( 
                decoded 
            )

    class _Recommender(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            country = body.get('country')

            countryList = ["global", "us"]
            countryNum = 0
            for i in range(len(countryList)):
                if country == countryList[i]:
                    countryNum = i 
            countryNum += 1
                
            
            country_songs = loadCountrySong("data/test/country_song.dat")
            print("country_song: " + str(country_songs))

            song_retriever = SongRetriever()
            song_retriever.loadSongs("data/test/song.dat")

            # use alternating least squares
            implict_model = implicit.als.AlternatingLeastSquares(
                factors=50, iterations=10, regularization=0.01
            )

            
            recommender = ImplicitRecommender(song_retriever, implict_model)
            # train
            recommender.fit(country_songs)
            print("country songs: " + str(country_songs))
            songs, scores = recommender.recommend(countryNum, country_songs, 3)
            
            songReturn = {}
            i = 0
            for song, score in zip(songs, scores):
                print(f"{song}: {score}")
                songReturn[i] = song 
                i += 1
                
            print(songReturn)

            return jsonify(songReturn)

            

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Login, '/login')
    api.add_resource(_Info, '/info')  
    api.add_resource(_Recommender, '/recommender')  