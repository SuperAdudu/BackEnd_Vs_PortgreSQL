from source.main.models.images import Images
from source.main.models.albums import Albums
from source.main.models.idols import Idols
from source import db
from flask import request, jsonify,send_from_directory
import os
from werkzeug.utils import secure_filename
import uuid

UPLOAD_FOLDER = os.path.abspath('media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://127.0.0.1:5000'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def addImage():
    try:
        data = request.form
        album = Albums.query.filter(Albums.id == data['idAlbum']).first()
        idol = Idols.query.filter(Idols.id==data['idModel']).first()
        files = request.files.getlist('images') 
        if not files:
            return jsonify({"status": 400, "message": "No files provided"})
        if album and idol:
            for file in files:
                if file and allowed_file(file.filename):

                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    new_filename = f"{uuid.uuid4().hex}.{file_extension}"

                    idol_folder = os.path.join(UPLOAD_FOLDER, idol.name)
                    album_folder = os.path.join(idol_folder, album.name)

                    os.makedirs(album_folder, exist_ok=True)

                    file_path = os.path.join(album_folder, new_filename)
                    file.save(file_path)
                    image_url = f"{BASE_URL}/media/{idol.name}/{album.name}/{new_filename}"
                else:
                    image_url = None
                new_image = Images(
                    idModel=data['idModel'],
                    idAlbum=data['idAlbum'],
                    link=image_url
                )
                db.session.add(new_image)
            db.session.commit()
            return jsonify({"status":200,"message":"Add image successfull"})
        else:
            return jsonify({"status":400,"message":"One of idInput is not correct"})    
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def viewImage(fileName,idolName,albumName):
    try:
        folder = os.path.join(UPLOAD_FOLDER, idolName, albumName)
        return send_from_directory(folder, fileName)
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def getImageByAlbum():
    try:
        data = request.form
        images = Images.query.filter(Images.idAlbum==data['idAlbum']).all()
        if images:
            result = []
            for image in images:
                result.append({
                    "idImage":image.id,
                    "idModel":image.idModel,
                    "link":image.link
                })
            return jsonify({"status":200,"data":result})
        else:
            return jsonify({"status":200,"message":"idAlbum is not correct"})
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
