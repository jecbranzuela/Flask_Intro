from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, SubmitField,IntegerField,FloatField,SelectField,HiddenField,BooleanField,PasswordField
from wtforms.validators import Length,DataRequired, EqualTo,ValidationError
from datetime import datetime

class LoginForm(FlaskForm):
    name=StringField(label='Name:',validators=[DataRequired()])
    password=PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class UserForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2,max=200), DataRequired()])
    description = StringField('Description')
    birthDate = DateField(label='Date of Birth:', validators=[DataRequired()], default=datetime.today().date)
    password1 = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Submit')

class ItemForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2,max=200), DataRequired()])
    price = IntegerField(label='Price:',validators=[DataRequired()])
    description = StringField('Description')
    type = StringField('Description')
    submit = SubmitField(label='Submit')

class ElectronicsForm(ItemForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])

class ClothingForm(ItemForm):
    brand = StringField('Brand', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])

class FoodForm(ItemForm):
    brand = StringField('Brand', validators=[DataRequired()])
    isHalalCertified = BooleanField('Halal Certified')

class PurchaseForm(FlaskForm):
    itemToBuy = SelectField('Item',choices = [], validators=[DataRequired()])
    buyer = SelectField(u'Buyer:', choices = [], validators=[DataRequired()])
    datePurchased = DateField('Date Purchased: ', validators=[DataRequired()], default=datetime.today().date)
    submit = SubmitField('Submit')