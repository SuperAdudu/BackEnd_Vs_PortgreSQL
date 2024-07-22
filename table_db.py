from source import db, create_app

app = create_app()

with app.app_context():
    
    from source.main.models.users import Users
    from source.main.models.idols import Idols
    from source.main.models.images import Images
    from source.main.models.albums import Albums
    db.create_all()
    print("Tables created successfully")