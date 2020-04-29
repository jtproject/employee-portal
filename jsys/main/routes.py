from flask import render_template, url_for, request, Blueprint, redirect
from jsys.models import TheCalendar, TheDays, Employee, Schedule
from flask_login import current_user
from jsys import _D, utils
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        # figure out what day it is
        now = datetime.now()
        this_month = TheCalendar.query.filter_by(the_year=now.year,the_month=int(now.month)).first()
        this_day = TheDays.query.filter_by(calid=this_month, day_num=now.day).first()
        # data to display
            # this week's schedule
        work_this = Schedule.query.filter_by(emp_id=current_user.id).filter(Schedule.work_date>=this_day.id, Schedule.work_date<=this_day.id+6).order_by(Schedule.work_date).all()
            # next week's schedule
        work_next = Schedule.query.filter_by(emp_id=current_user.id).filter(Schedule.work_date>=this_day.id+7, Schedule.work_date<=this_day.id+13).order_by(Schedule.work_date).all()
    else:
        work_this = 'NOTHING'
        work_next = 'Nope'
    return render_template('home.html', work=work_this, work2=work_next, title='Home', utils=utils)

@main.route('/new', methods=['GET', 'POST'])
def new():
    return render_template('shell.html', title='Build Test')
