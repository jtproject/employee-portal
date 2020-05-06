from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from jsys import utils

class AddEventForm(FlaskForm):
    event_my_opt = SelectField('Month/Year', validators=[DataRequired()], choices=[])
    event_day = StringField('Day', validators=[DataRequired()])
    event_name = StringField('Event Name', validators=[DataRequired()])
    event_desc = TextAreaField('Rentals and Notes')
    setup_my_opt = SelectField('Month/Year', choices=[])
    setup_day = StringField('Day')
    pickup_my_opt = SelectField('Month/Year', choices=[])
    pickup_day = StringField('Day')
    odd_setup = StringField('After Hour Setup')
    odd_pickup = StringField('After Hour Pickup')
    submit = SubmitField('Add')
    submit2 = SubmitField('Update')

    def validate(self):
        return True
