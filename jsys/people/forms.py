from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from jsys.models import Employee
from jsys import utils

class RegGuy(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    num = StringField('Cell #', validators=[DataRequired()])
    pw = PasswordField('Create Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('pw')])
    submit = SubmitField('Join')

    def validate_num(self, num):
        try:
            num.data = utils.phone_strip(num.data)
        except:
            print('Bad value')
            raise ValidationError('Invalid format')

    def validate_email(self, email):
        g = Employee.query.filter_by(email=email.data).first()
        if g:
            print(g)
            raise ValidationError('This email belongs to ' + g.first_name + ' ' + g.last_name + '.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    pw = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAvailabilityForm(FlaskForm):
    choose = [('1','All Day'),('2','Need Off'),('3','Late Start'),('4','Early Out'),('5','Custom')]

    monday_opt = SelectField('Monday', validators=[DataRequired()], choices=choose)
    tuesday_opt = SelectField(validators=[DataRequired()], choices=choose)
    wednesday_opt = SelectField(validators=[DataRequired()], choices=choose)
    thursday_opt = SelectField(validators=[DataRequired()], choices=choose)
    friday_opt = SelectField(validators=[DataRequired()], choices=choose)
    saturday_opt = SelectField(validators=[DataRequired()], choices=choose)
    sunday_opt = SelectField(validators=[DataRequired()], choices=choose)
    submit = SubmitField('Update')

    def validate(self):
        return True


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')
