from Automotive_Shop_app.application import create_app
from Automotive_Shop_app.application.models import db

app = create_app('ProductionConfig')

with app.app_context():
     #db.drop_all()
     db.create_all()

#app.run() 
