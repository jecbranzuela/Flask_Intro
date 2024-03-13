from static import db #import the db which can be found in __init__
from datetime import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False, default = 50)
    datePurchased = db.Column(db.Date, default = datetime.utcnow)
    #type = db.Column(db.String(50), nullable = False)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(), nullable = False)
    birthDate = db.Column(db.Date, default = datetime.utcnow)