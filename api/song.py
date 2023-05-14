import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import Song

song_api = Blueprint('song_api', __name__,
                   url_prefix='/api/songs')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(song_api)

class SongAPI:        
    class _Song(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 1:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400

            # validate name
            song = body.get('song')
            """
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            """

            ''' #1: Key code block, setup USER OBJECT '''
            addSong = Song(uid=uid, song=song)
            
            ''' Additional garbage error checking '''
            """
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            """
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            outputSong = addSong.create()
            # success returns json of user
            if outputSong:
                return jsonify(outputSong.read())
            # failure returns error
            return {'message': f'Processed {song}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method
            songs = Song.query.all()    # read/extract all users from database
            json_ready = [song.read() for song in songs]  # prepare output in json
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

            

    # building RESTapi endpoint
    api.add_resource(_Song, '/test')
    