import os
from flask import request, jsonify
from musicapp import app
from flask_restful import Api, Resource, reqparse
from musicapp.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user
from mutagen.mp3 import MP3


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
            db.session.add(user)
            db.session.commit()
            return {'message': 'Account successfully created for user.'}, 201
        

api.add_resource(UserRegistration, '/api/register')


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Please provide a value')
login_parser.add_argument('password', type=str, required=True, help='Please provide a value')


class UserLogin(Resource):
    def post(self):
        args = login_parser.parse_args()
        hashed_password = generate_password_hash(args['password'])
        user = User.query.filter_by(username=args['username']).first()
        check_password_hash(hashed_password, args['password'])
        if user and check_password_hash:
            return {'message': 'Login successful.'}, 201
        else:
            return {'message': 'Incorrect username or password.'}, 404


api.add_resource(UserLogin, '/api/login')


class AdminLogin(Resource):
    def post(self):
        args = login_parser.parse_args()
        if args['username']=='admin' and  args['password']=='admin':
            return {'message': 'You are now logged in as admin.'}, 201
        else:
            return {'message': 'Incorrect username or password.'}, 404
        
api.add_resource(AdminLogin, '/api/admin_login')      


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



api.add_resource(CreatorRegistration, '/api/register_creator/<int:user_id>')

#============================================== USER =====================================================

profile_parser = reqparse.RequestParser()
profile_parser.add_argument('name', type=str, required=True, help='Please provide a value')
profile_parser.add_argument('username', type=str, required=True, help='Please provide a value')
profile_parser.add_argument('current_password', type=str, required=True, help='Please provide a value')
profile_parser.add_argument('new_password', type=str, required=True, help='Please provide a value')

class UpdateProfile(Resource):
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
                return {'message': 'Profile successfully updated.'}, 201
            else:
                return {'message': 'Incorrect current password.'}, 404
        else:
            return {'message': 'User not found.'}, 404
        

api.add_resource(UpdateProfile, '/api/update_profile/<int:user_id>')

# ================================================= SONGS ===================================================

class SongListResource(Resource):
    def get(self):
        songs = Song.query.filter_by(is_flagged=False).order_by(Song.timestamp.desc()).all()
        songs_list = []
        for song in songs:
            artist = Artist.query.get(song.artist_id)
            song_data = {'id': song.id, 'title': song.title, 'filename': song.filename, 'duration': song.duration, 'lyrics': song.lyrics, 'artist': artist.name}
            songs_list.append(song_data)

        return {'songs': songs_list}, 201    
    
    def post(self):
        args = song_parser.parse_args()
        artist_id = Artist.query.filter(name=args['artist'])
        song = Song(title=args['title'], lyrics=args['lyrics'], artist_id=artist_id)

        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        duration = get_audio_duration(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        song.duration = duration

        db.session.add(song)
        db.session.commit()

        return {
                'message': 'File successfully uploaded'
                # 'title': song.title,
                # 'filename': song.filename,
                # 'artist_id': song.artist_id,
                # 'duration': song.duration
            }, 201

    
api.add_resource(SongListResource, '/api/songs')    


song_parser = reqparse.RequestParser()
song_parser.add_argument('title', type=str)
song_parser.add_argument('artist', type=str)
song_parser.add_argument('lyrics', type=str)

class SongResource(Resource):
    def get(self, song_id):
        song = Song.query.get(song_id)
        if song:
            artist = Artist.query.get(song.artist_id)
            song_data = {'id': song.id, 'title': song.title, 'filename': song.filename, 'duration': song.duration, 'lyrics': song.lyrics, 'artist': artist.name}
            return {'song': song_data}, 201
        else:
            return {'message': 'Song not found'}, 404 
        

    def put(self, song_id):
        args = song_parser.parse_args()
        song = Song.query.get(song_id)
        song.title = args['title']
        song.lyrics = args['lyrics']
        artist = Artist.query.get(song.artist_id)
        song.artist_id = artist.id
        db.session.commit()
        return {'message': 'Song updated successfully'}, 201
    
    def delete(self, song_id):
        song = Song.query.get(song_id)
        if song:
            db.session.delete(song)
            db.session.commit()
            return {'message': 'Song deleted successfully'}, 200
        else:
            return {'message': 'Song not found'}, 404


    
api.add_resource(SongResource, '/api/song/<int:song_id>')


# filter_parser = reqparse.RequestParser()
# filter_parser.add_argument('filter_type', type=str, choices=('title', 'artist', 'rating') ,required=True, help='Please provide a value')
# filter_parser.add_argument('filter_value', type=str, required=True, help='Please provide a value')

# class FilteredSongs(Resource):
#     args = filter_parser.parse_args()
#     filter_type = args['filter_type']
#     filter_value = args['filter_value']

#     if filter_value:
#             if filter_type == 'artist':
#                 songs = songs.join(Artist).filter(Artist.name.ilike(f"%{filter_value}%"))
#             elif filter_type == 'title':
#                 songs = songs.filter(Song.title.ilike(f"%{filter_value}%"))
#             elif filter_type == 'rating':
#                 try:
#                     rating = float(filter_value)
#                     songs = songs.join(Interactions).group_by(Song.id).having(db.func.avg(Interactions.rating) == rating)
#                 except ValueError:
#                     flash('Invalid rating value. Please enter a numeric value.', 'danger')


# =============================================== PLAYLISTS ===================================================

class PlaylistListResource(Resource):
    def get(self):
        playlists = Playlist.query.order_by(Playlist.timestamp.desc()).all()
        playlists_list = []
        for playlist in playlists:
            playlist_data = {'id': playlist.id, 'name': playlist.name}
            playlists_list.append(playlist_data)

        return {'playlists': playlists_list}, 201    
    

api.add_resource(PlaylistListResource, '/api/playlists')

playlist_parser = reqparse.RequestParser()
playlist_parser.add_argument('name', type=str, required=True, help='Please provide a value')


class PlaylistResource(Resource):
    def get(self, playlist_id):
        playlist = Playlist.query.get_or_404(playlist_id)
        if playlist:
            playlist_data = {'id': playlist.id, 'name': playlist.name}
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


api.add_resource(PlaylistResource, '/api/playlist/<int:playlist_id>')



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
        

api.add_resource(AlbumListResource, '/api/albums')    

album_parser = reqparse.RequestParser()
album_parser.add_argument('name', type=str, required=True, help='Please provide a value')
album_parser.add_argument('genre', type=str, choices=('Pop', 'Metal', 'Classical', 'Other'), default='Other')
album_parser.add_argument('artist', type=str, required=True, help='Please provide a value')


class AlbumResource(Resource):
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        if album:
            artist = Artist.query.get_or_404(album.artist_id)
            album_data = {'id': album.id, 'name': album.name, 'genre': album.genre, 'artist': artist.name}
            return {'album': album_data}, 201
        else:
            return {'message': 'Album not found.'}

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
        


api.add_resource(AlbumResource, '/api/album/<int:album_id>')