
from application.models import Album



def csv_details(creator_id):
    albums = Album.query.filter_by(creator_id=creator_id).all()
    res=[]
    for album in albums:
        res.append((album.id,album.name,album.genre,album.artist_name,album.album_songs))

    return res