from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from jsys import utils
import pickle

class AddWorkForm(FlaskForm):
    worker = SelectField(u'Employee', validators=[DataRequired()], choices=[])
    month_year_opt = SelectField(u'Month / Year', choices=[])
    day_field = StringField('Day', validators=[DataRequired()])
    work_status = RadioField(validators=[DataRequired()], choices=[('ON', 'Working'),('OFF', 'Off')], default='ON')
    submit = SubmitField('Add')

    def validate(self):
        return True
