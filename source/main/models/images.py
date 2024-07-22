from source import db

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModel = db.Column(db.Integer, nullable=False)
    idAlbum = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(250), unique=True, nullable=False)