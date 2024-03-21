from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt #hash the password from user

app = Flask(__name__)
login_manager=LoginManager(app)
login_manager.login_view = "login_page"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SECRET_KEY'] = '54d4ba538a7892d0e826d4ac'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #bcrypt will generate hash passwords rather than storing them as plain text
from static import routes