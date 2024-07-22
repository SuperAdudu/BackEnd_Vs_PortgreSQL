from source import db

class Idols(db.Model):
    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    linkAvatar = db.Column(db.String(250), nullable=True)