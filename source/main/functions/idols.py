from source.main.models.idols import Idols
from flask import jsonify, request,send_from_directory
from source import db 
import os
import uuid

UPLOAD_FOLDER = os.path.abspath('media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://127.0.0.1:5000'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getAllIdols():
    try:
        idols = Idols.query.all()
        data = []
        for idol in idols:
            data.append({"id":idol.id,"name":idol.name})
        return jsonify({'status':200,'data':data})
    except Exception as e:
        return jsonify({'status':404,'message':str(e)})
    
def addIdols():
    try:
        data = request.form
        idol = Idols(name=data['name'])
        db.session.add(idol)
        db.session.commit()
        return jsonify({'status':200,'message':'Add idol successful'})
    except Exception as e:
        return jsonify({'status':404,'message':str(e)})
    
def changeAvatar():
    try:
        data = request.form
        idol = Idols.query.filter(Idols.id==data['id']).first()
        if not idol:
            return jsonify({"status":400,"message":"Id is not correct"})    
        file = request.files['avatar'] if 'avatar' in request.files else None
        if file and allowed_file(file.filename):

            file_extension = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{file_extension}"

            avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatar')
            user_avatar_folder = os.path.join(avatar_folder, 'idol')

            os.makedirs(user_avatar_folder, exist_ok=True)

            file_path = os.path.join(user_avatar_folder, new_filename)
            file.save(file_path)
            image_url = f"{BASE_URL}/media/avatar/idol/{new_filename}"
        else:
            image_url = None
        idol.linkAvatar = image_url
        db.session.commit()
        result = {}
        result['id'] = idol.id
        result['name'] = idol.name
        result['linkAvatar'] = idol.linkAvatar
        return jsonify({"status":200,"data":result})     
    except Exception as e:
        return jsonify({"status":404,"error":str(e)})
    
def viewAvatarIdol(fileName):
    try:
        folder = os.path.join(UPLOAD_FOLDER, 'avatar', 'idol')
        return send_from_directory(folder, fileName)
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})