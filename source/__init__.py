from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.abspath('media')
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    
    from source.main.controllers import register_routes
    register_routes(app)
    
    return app

