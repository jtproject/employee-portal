from flask import render_template, url_for, request, Blueprint, redirect
from jsys.models import TheCalendar, Employee, Schedule
from flask_login import current_user
from jsys import _D, utils

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        work = Schedule.query.filter_by(emp_id=current_user.id).all()
    else:
        work = 'NOTHING'
    return render_template('home.html', work=work, title='Home', utils=utils)

@main.route('/new', methods=['GET', 'POST'])
def new():
    return render_template('shell.html', title='Build Test')
