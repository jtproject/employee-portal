from flask import render_template, url_for, request, Blueprint, redirect
from jsys.models import TheCalendar, TheDays, Employee, Schedule, Event
from flask_login import current_user
from jsys import _D, utils, dataf
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        this_day = dataf.today()
        # data to display
            # this week's schedule
        work_this = Schedule.query.filter_by(emp_id=current_user.id).filter(Schedule.work_date>=this_day.id, Schedule.work_date<=this_day.id+6).order_by(Schedule.work_date).all()
            # next week's schedule
        #work_next = Schedule.query.filter_by(emp_id=current_user.id).filter(Schedule.work_date>=this_day.id+7, Schedule.work_date<=this_day.id+13).order_by(Schedule.work_date).all()
            # this month's events
        event_month = Event.query.filter(Event.event_date>=this_day.id, Event.event_date<=this_day.id+30).order_by(Event.event_date).all()
    else:
        work_this = 'NOTHING'
        work_next = 'Nope'
        event_month = 'Dang'
    return render_template('home.html', work=work_this, job=event_month, title='Home', utils=utils)

@main.route('/new', methods=['GET', 'POST'])
def new():
    return render_template('shell.html', title='Build Test')
