from source import db

class Albums(db.Model):
    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idModel = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)