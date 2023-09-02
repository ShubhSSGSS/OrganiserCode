from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateTimeLocalField
from wtforms.validators import data_required, length, equal_to, number_range, ValidationError
from codeDir.models import User
from flask_wtf.file import FileField, FileAllowed


class signUpForm(FlaskForm):

    usernameField = StringField('Username: ', validators=[data_required(), length(min=3, max=20)])
    pinField = IntegerField('Pin: ', validators=[data_required(), number_range(min=1000, max=9999)])
    confirmPinField = IntegerField('Confirm your pin: ', validators=[data_required(), equal_to('pinField')])
    submitButton = SubmitField('Sign up')

    def validate_usernameField(self, usernameField):
        checkDupUser = User.query.filter_by(username=usernameField.data)

        if len(checkDupUser.all()) > 0:
            raise ValidationError('Username already exists!')
        
class logInForm(FlaskForm):

    usernameField = StringField('Username: ', validators=[data_required(), length(min=3, max=20)])
    pinField = IntegerField('Pin: ', validators=[data_required(), number_range(min=1000, max=9999)])
    submitButton = SubmitField('Log in')

    def validate_pinField(self, pinField):
        userPin = User.query.filter_by(username=self.usernameField.data).with_entities(User.userPin).all()[0][0]
        if userPin != pinField.data:
            raise ValidationError('Incorrect password.')
        
class planForm(FlaskForm):

    planNameField = StringField('Plan Name: ', validators=[data_required(), length(min=1, max=60)])
    planDescField = StringField('Description: ', validators=[length(min=1, max=200)])
    planTimeField = DateTimeLocalField('Time: ', format='%Y-%m-%dT%H:%M', validators=[data_required()])
    planLocField = StringField('Location: ', validators=[data_required()])
    submitButton = SubmitField('Create Plan')
