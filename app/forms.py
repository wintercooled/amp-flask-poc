from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisteredUserForm(FlaskForm):
    name = StringField('Registered User Name/Reference', validators=[DataRequired()])
    gaid = StringField('Green Wallet AMP Account ID')
    submit = SubmitField('Add Registered User')
