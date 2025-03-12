from app import create_app
from app.models import db

app = create_app('DevelopmetConfig')

with app.app_context():
    db.create_all()

app.run()