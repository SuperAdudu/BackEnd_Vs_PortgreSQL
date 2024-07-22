from source.main.models.albums import Albums
from flask import jsonify,request
from source import db

def getAllAlbum():
    try:
        data = request.form
        albums = Albums.query.filter(Albums.idModel==data['idModel']).all()
        if albums:
            data_result = []
            for album in albums:
                data_result.append({
                    "idAlbum": album.id,
                    "name": album.name
                })
            return jsonify({"status":200,"data":data_result})
        else:
            return jsonify({"status":200,"message":"No album"})
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def createAlbum():
    try:
        data = request.form
        new_album = Albums(
            idModel=data['idModel'],
            name=data['name']
        )
        db.session.add(new_album)
        db.session.commit()
        return jsonify({"status":200,"message":"Add album successfull!"})
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})