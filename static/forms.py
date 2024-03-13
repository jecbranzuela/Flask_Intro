from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField, SubmitField,IntegerField,FloatField,SelectField,HiddenField
from wtforms.validators import Length,DataRequired, EqualTo,ValidationError

class RegisterItemForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2,max=200), DataRequired()])
    price = IntegerField(label='Price:',validators=[DataRequired()])
    datePurchased = DateField(label='Date Purchased:', validators=[DataRequired()])
    type = SelectField("Type:", choices=[('Electronic'),('Medicine'),('Food'),('Misc')],validators=[DataRequired()])
    submit = SubmitField(label='Submit')