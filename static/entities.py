from static import db,bcrypt,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association Table for M2M relationship
item_user_association = db.Table(
    'item_user_association',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), nullable=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=True),
    db.Column('datePurchased', db.Date, default=datetime.now)
)

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=50)
    description = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(50))

    # Define the many-to-many relationship with User
    owners = db.relationship('User', secondary=item_user_association, backref=db.backref('items_owned', lazy='dynamic'),overlaps="items_owned,owners")

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(), nullable=False)
    passwordHash = db.Column(db.String(length=60),nullable=False)
    birthDate = db.Column(db.Date, default=datetime.utcnow)

    # Define the many-to-many relationship with Item
    owned_items = db.relationship('Item', secondary=item_user_association, backref=db.backref('purchasors', lazy='dynamic'),overlaps="items_owned,owners")

    def checkPassword(self,attemptedPassword):
        userPass = User.query.filter_by(id=self.id).first()
        if userPass.passwordHash == attemptedPassword:
            return True
        return False
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.passwordHash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

class Electronics(Item):
    __tablename__ = 'electronics'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    manufacturer = db.Column(db.String(), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'electronics',
    }

class Clothing(Item):
    __tablename__ = 'clothing'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    brand = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'clothing',
    }

class Food(Item):
    __tablename__ = 'food'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    brand = db.Column(db.String(), nullable=False)
    isHalalCertified = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'food',
    }
