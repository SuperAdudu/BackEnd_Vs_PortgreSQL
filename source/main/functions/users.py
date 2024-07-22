from source import db
from source.main.models.users import Users
from flask import jsonify, request, send_from_directory
from sqlalchemy.exc import IntegrityError
import os
import uuid
import  re

UPLOAD_FOLDER = os.path.abspath('media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://127.0.0.1:5000'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False

def registerUser():
    try:
        data = request.form
        file = request.files['avatar'] if 'avatar' in request.files else None
        if not is_valid_email(data['email']):
            return jsonify({"error": "Invalid email format!"})

        if file and allowed_file(file.filename):

            file_extension = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{file_extension}"

            avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatar')
            user_avatar_folder = os.path.join(avatar_folder, 'user')

            os.makedirs(user_avatar_folder, exist_ok=True)

            file_path = os.path.join(user_avatar_folder, new_filename)
            file.save(file_path)
            image_url = f"{BASE_URL}/media/avatar/user/{new_filename}"
        else:
            image_url = None
        new_user = Users(
            username = data['username'],
            email = data['email'],
            link = image_url
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            result = {}
            result['idUser'] = new_user.id
            result['username'] = new_user.username
            result['email'] = new_user.email
            result['link'] = new_user.link
            return jsonify({"status":200,"data":result})
        except IntegrityError as e:
            db.session.rollback() 
            os.remove(file_path) 
            if "Duplicate entry" in str(e.orig):
                return jsonify({"error": "Email already exists!"}), 400
            return jsonify({"error": "An error occurred during registration."})
        
    except Exception as e:
        os.remove(file_path) 
        return jsonify({"status":404,"error":str(e)})
    
def viewAvatarUser(fileName):
    try:
        folder = os.path.join(UPLOAD_FOLDER, 'avatar', 'user')
        return send_from_directory(folder, fileName)
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})