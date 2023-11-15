from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField
from wtforms.validators import DataRequired,Email,Length

class ContactFrom(FlaskForm):
    fname = StringField('Firstname',validators=[DataRequired()])
    lname = StringField('Lastname',validators=[DataRequired()])
    email = StringField('Your Email',validators=[Email()])
    password=PasswordField('Your Password',validators=[DataRequired(),Length(8)])
    country= StringField('Your Country',validators=[DataRequired()])
    btn = SubmitField('Send Message')
    

class ContactUs(FlaskForm):
    name =StringField('Fullname',validators=[DataRequired()])
    phone =StringField('Phone',validators=[DataRequired()])
    email =StringField('Your Email',validators=[Email()])
    message =TextAreaField('message')
    btn = SubmitField('Send Message')
    
