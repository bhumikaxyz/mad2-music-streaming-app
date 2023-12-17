import os
import secrets
from functools import wraps
from flask import request, jsonify, make_response
from application import app
from flask_restful import Api, Resource, reqparse, marshal_with, fields, marshal
from application.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user
from mutagen.mp3 import MP3
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_current_user, verify_jwt_in_request


def get_audio_duration(file_path):
    try: 
       
        audio = MP3(file_path)
        duration_in_seconds = audio.info.length
        minutes, seconds = divmod(duration_in_seconds, 60)
        duration = f"{int(minutes):02}:{int(seconds):02}"
        return duration
    except:
        return None 


api = Api()
api.prefix = '/api'    

from application import jwt

#----------------------------------------- Output Fields ---------------------------------------------------

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'password_hash': fields.String,
    'is_creator': fields.Boolean,
    'is_flagged': fields.Boolean,
    'fs_uniquifier': fields.String,
    'active': fields.Boolean
}

song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'filename': fields.String,
    'duration': fields.String,
    'lyrics': fields.String,   
    'album_id': fields.Integer,
    'artist_id': fields.Integer,
    'creator_id': fields.Integer,
    'timestamp': fields.DateTime(dt_format='rfc822'),
    'is_flagged': fields.Boolean

}

# =======================================================================
# @jwt.user_lookup_loader()
def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            roles = role if isinstance(role, list) else [role]
            print(current_user)
            for r in roles:
                print(current_user.roles)
                print(current_user.has_role(r), r)
            if all(not current_user.has_role(r) for r in roles):
                return make_response({"message": f"Missing any of roles {','.join(roles)}"}, 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

    
#======================================= Registration and Login =========================================

register_parser = reqparse.RequestParser()
register_parser.add_argument('name', type=str, required=True, help='Please provide a value')
register_parser.add_argument('username', type=str, required=True, help='Please provide a value')
register_parser.add_argument('password', type=str, required=True, help='Please provide a value')
register_parser.add_argument('confirm_password', type=str, required=True, help='Please provide a value')


class UserRegistration(Resource):
    def post(self):
        args = register_parser.parse_args()

        if args['password'] != args['confirm_password']:
            return {'message': 'Password and Confirm Password do not match.'}
        
        existing_user = User.query.filter_by(username=args['username']).first()

        if existing_user:
            return {'message': 'User already exists.'}, 404
        else:
            hashed_password = generate_password_hash(args['password'])
            user = User(name=args['name'], username=args['username'], password_hash=hashed_password)
            user.fs_uniquifier = secrets.token_hex(16)
            db.session.add(user)
            db.session.commit()
            return {'message': 'Successfully registered'}, 201
        

api.add_resource(UserRegistration, '/register')


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Please provide a value')
login_parser.add_argument('password', type=str, required=True, help='Please provide a value')


class UserLogin(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password =args['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if user.is_flagged:
                return {'message': 'You are not allowed to use this platform'}, 404
            else:
                check_password_hash(user.password_hash, password)
                if check_password_hash:
                    access_token = create_access_token(identity=user.id)
                    return jsonify({'status': 'success','message': 'Successfully logged in !!', 'access_token': access_token, "username": username})
                else:
                    return {'message': 'Incorrect username or password.'}, 404
        else:
            return {'message': 'Incorrect username or password.'}, 404   
       

api.add_resource(UserLogin, '/signin')


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity() 
        return jsonify({'status': 'success', 'message': f'Successfully logged out user: {current_user}'})

api.add_resource(UserLogout, '/signout')


#============================================== USER =====================================================

creator_register_parser = reqparse.RequestParser()
creator_register_parser.add_argument('response', type=bool, default=False)

class CreatorRegistration(Resource):
    def put(self, user_id):
        args = creator_register_parser.parse_args()
        user = User.query.get(user_id)
        if user and not user.is_creator:
            if args['response']:
                user.is_creator = True
                db.session.commit()
                return {'message': 'Account upgraded to creator.'}, 201
            else:
                return {'message': 'User account.'}, 201
        else:
            return {'message': 'NOTHING'}, 404    



api.add_resource(CreatorRegistration, '/register_creator/<int:user_id>')


profile_parser = reqparse.RequestParser()
profile_parser.add_argument('name', type=str)
profile_parser.add_argument('username', type=str)
profile_parser.add_argument('current_password')
profile_parser.add_argument('new_password')

class UpdateProfile(Resource):
    @marshal_with(user_fields)
    def put(self, user_id):
        args = profile_parser.parse_args()
        user = User.query.get(user_id)
        if user:
            if check_password_hash(user.password_hash, args['current_password']):
                user.name = args['name']
                user.username = args['username']
                hashed_password = generate_password_hash(args['new_password'])
                user.password_hash = hashed_password
                db.session.commit()
                return user, 201
            else:
                return {'message': 'Incorrect current password.'}, 404
        else:
            return {'message': 'User not found.'}, 404
        

api.add_resource(UpdateProfile, '/update_profile/<int:user_id>')


# ========================================== ADMIN ====================================================

class AdminLogin(Resource):
    def post(self):
        args = login_parser.parse_args()
        if args['username']=='admin' and  args['password']=='admin':
            return {'message': 'You are now logged in as admin.'}, 201
        else:
            return {'message': 'Incorrect username or password.'}, 404
        
api.add_resource(AdminLogin, '/admin_login')      


flag_parser = reqparse.RequestParser()
flag_parser.add_argument('response', type=bool, default=False)

class FlagSong(Resource):
    def put(self, song_id):
        args = flag_parser.parse_args()
        song = Song.query.get(song_id)
        if song:
            song.is_flagged = args['response']
            db.session.commit()
            return {'song': marshal(song, song_fields)}, 200
        else:
            return {'message': 'song not found.'}    
        

api.add_resource(FlagSong, '/flag_song/<int:song_id>')


class FlagCreator(Resource):
    def put(self, user_id):
        args = flag_parser.parse_args()
        creator = User.query.get(user_id)
        if creator:
            creator.is_flagged = args['response']
            db.session.commit()
            return {'user': marshal(creator, user_fields)}, 200
        else:
            return {'message': 'user not found.'}    
        
        

api.add_resource(FlagCreator, '/flag_creator/<int:user_id>')


# ================================================= SONGS ===================================================

class SongListResource(Resource):
    @auth_role(["creator", "admin"])
    @jwt_required()
    def get(self):
        songs = Song.query.filter_by(is_flagged=False).order_by(Song.timestamp.desc()).all()
        songs_list = []
        for song in songs:
            songs_list.append(marshal(song, song_fields))
    
        return {'songs': songs_list}, 201    
    

    @marshal_with(song_fields)
    def post(self):
        title = request.form.get("title")
        lyrics = request.form.get("lyrics")
        artist = request.form.get("artist")
        artist = Artist.query.filter_by(name=artist).first()
        song = Song(title=title, lyrics=lyrics, artist_id=artist.id)
       
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        song.filename = filename
        duration = get_audio_duration(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        song.duration = duration
        db.session.add(song)
        db.session.commit()
        return song, 201

    
api.add_resource(SongListResource, '/songs')    


song_parser = reqparse.RequestParser()
song_parser.add_argument('title', type=str)
song_parser.add_argument('artist', type=str)
song_parser.add_argument('lyrics', type=str)


class SongResource(Resource):
    def get(self, song_id):
        song = Song.query.get(song_id)
        if song:
            return {'song': marshal(song, song_fields)}, 201
        else:
            return {'message': 'Song not found'}, 404 
        

    def put(self, song_id):
        args = song_parser.parse_args()
        song = Song.query.get(song_id)
        song.title = args['title']
        song.lyrics = args['lyrics']

        artist = Artist.query.filter_by(name=args['artist']).first()
        if not artist:
            artist = Artist(name=args['artist'])
            db.session.add(artist)
            db.session.commit()

        song.artist_id = artist.id
        db.session.commit()
        return {'song': marshal(song, song_fields)}, 200
    

    def delete(self, song_id):
        song = Song.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
            return {'message': 'Song deleted successfully'}, 200
        else:
            return {'message': 'Song not found'}, 404


    
api.add_resource(SongResource, '/song/<int:song_id>')


filter_parser = reqparse.RequestParser()
filter_parser.add_argument('filter_type', type=str, choices=('title', 'artist', 'rating') ,required=True, help='Please provide a value')
filter_parser.add_argument('filter_value', type=str, required=True, help='Please provide a value')

class FilteredSongs(Resource):
    def get(self):
        args = filter_parser.parse_args()
        query = Song.query.filter_by(is_flagged=False).order_by(Song.timestamp.desc())
        # songs = Song.query.filter_by(is_flagged=False).order_by(Song.timestamp.desc()).all()
        filter_type = args['filter_type']
        filter_value = args['filter_value']

        if filter_type:
            if not filter_value:
                return {'message': 'Please specify a value to search'}, 404
            elif filter_value:
                    if filter_type == 'artist':
                        query = query.join(Artist).filter(Artist.name.ilike(f"%{filter_value}%"))
                    elif filter_type == 'title':
                        query = query.filter(Song.title.ilike(f"%{filter_value}%"))
                    elif filter_type == 'rating':
                        try:
                            rating = float(filter_value)
                            query = query.join(Interactions).group_by(Song.id).having(db.func.avg(Interactions.rating) == rating)
                        except ValueError:
                            return {'message': 'Invalid rating value.'}, 404
                           
        filtered_songs = query.all()
        songs_list = []
        for song in filtered_songs:
            songs_list.append(marshal(song, song_fields))

        return {'songs': songs_list}, 201    

api.add_resource(FilteredSongs, '/songs/filter')


like_parser = reqparse.RequestParser()
like_parser.add_argument('like', type=bool, default=False)

class LikeSongResource(Resource):
    def post(self, song_id):
        args = like_parser.parse_args()
        song = Song.query.get(song_id)
        # user = current_user
        like = args['like']
        existing_interaction = Interactions.query.filter_by(song_id=song.id).first()
        if existing_interaction:
            existing_interaction.liked = args['like']
        else:
            new_interaction = Interactions(song_id=song.id, liked=like)
            db.session.add(new_interaction)

        db.session.commit()
        return {'song': marshal(song, song_fields)}, 200

api.add_resource(LikeSongResource, '/like/<int:song_id>')


rating_parser = reqparse.RequestParser()
rating_parser.add_argument('rating', type=float, choices=[1, 2, 3, 4, 5], default=0)

class RateSongResource(Resource):
    def post(self, song_id):
        args = rating_parser.parse_args()
        song = Song.query.get(song_id)
        # user = current_user
        rating = args['rating']
        existing_interaction = Interactions.query.filter_by(song_id=song.id).first()
        if existing_interaction:
            existing_interaction.rating = rating
        else:
            new_interaction = Interactions(song_id=song.id, rating=rating)
            db.session.add(new_interaction)

        db.session.commit()
        return {'song': marshal(song, song_fields)}, 200

api.add_resource(RateSongResource, '/rate/<int:song_id>')


# =============================================== PLAYLISTS ================================================

class PlaylistListResource(Resource):
    def get(self):
        playlists = Playlist.query.order_by(Playlist.timestamp.desc()).all()
        playlists_list = []
        for playlist in playlists:
            playlist_data = {'id': playlist.id, 'name': playlist.name}
            playlists_list.append(playlist_data)

        return {'playlists': playlists_list}, 201    
    

api.add_resource(PlaylistListResource, '/playlists')

playlist_parser = reqparse.RequestParser()
playlist_parser.add_argument('name', type=str, required=True, help='Please provide a value')


class PlaylistResource(Resource):
    def get(self, playlist_id):
        playlist = Playlist.query.get_or_404(playlist_id)
        if playlist:
            song_list = [song for song in playlist.songs]
            playlist_data = {'id': playlist.id, 'name': playlist.name, 'songs': song_list}
            return {'playlist': playlist_data}, 201
        else:
            return {'message': 'Playlist not found.'}, 404

    def put(self, playlist_id):
        args = playlist_parser.parse_args()
        playlist = Playlist.query.get_or_404(playlist_id)
        if playlist:
            playlist.name = args['name']
            db.session.commit()
            return {'message': 'Playlist updated successfully'}, 201
        else:
            return {'message': 'Playlist not found'}, 404

    def delete(self, playlist_id):
        playlist = Playlist.query.get_or_404(playlist_id)
        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            return {'message': 'Playlist deleted successfully'}, 201
        else:
            return {'message': 'Playlist not found'}, 404  


api.add_resource(PlaylistResource, '/playlist/<int:playlist_id>')



#============================================= ALBUMS =====================================================

class AlbumListResource(Resource):
    def get(self):
        albums = Album.query.order_by(Album.timestamp.desc()).all()
        albums_list = []
        for album in albums:
            artist = Artist.query.get(album.artist_id)
            album_data = {'id': album.id, 'name': album.name, 'genre': album.genre, 'artist': artist.name}
            albums_list.append(album_data)

        return {'albums': albums_list}, 201    
        

api.add_resource(AlbumListResource, '/albums')    

album_parser = reqparse.RequestParser()
album_parser.add_argument('name', type=str, required=True, help='Please provide a value')
album_parser.add_argument('genre', type=str, choices=('Pop', 'Metal', 'Classical', 'Other'), default='Other')
album_parser.add_argument('artist', type=str, required=True, help='Please provide a value')


class AlbumResource(Resource):
    def get(self, album_id):
        print("hiii")
        album = Album.query.get(album_id)
        print(album)
        if album:
            artist = Artist.query.get(album.artist_id)
            album_data = {'id': album.id, 'name': album.name, 'genre': album.genre, 'artist': artist.name, 'songs': album.songs}
            return {'album': album_data}, 201
        else:
            return {'message': 'Album not found.'}, 404

    def put(self, album_id):
        args = album_parser.parse_args()
        album = Album.query.get_or_404(album_id)
        if album:
            album.name = args['name']
            album.genre = args['genre']
            artist = Artist.query.filter_by(name=args['artist']).first()
            album.artist_id = artist.id
            db.session.commit()
            return {'message': 'Album updated successfully'}, 201
        else:
            return {'message': 'Album not found'}, 404



    def delete(self, album_id):
        album = Album.query.get(album_id)
        if album:
            db.session.delete(album)
            db.session.commit()
            return {'message': 'Album deleted successfully'}, 201
        else:
            return {'message': 'Album not found'}, 404
        

api.add_resource(AlbumResource, '/album/<int:album_id>')