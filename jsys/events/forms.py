from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from jsys import utils

class AddEventForm(FlaskForm):
    month_year_opt = SelectField('Month/Year', validators=[DataRequired()], choices=[])
    day_field = StringField('Day', validators=[DataRequired()])
    submit = SubmitField('Add')
