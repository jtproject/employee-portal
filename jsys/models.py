from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Ser
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from jsys import _D, _X, _L, utils

@_L.user_loader
def uLoad(u_id):
    return Employee.query.get(int(u_id))

class Employee(_D.Model, UserMixin):
    id = _D.Column(_D.Integer, primary_key=True)
    first_name = _D.Column(_D.String(20), nullable=False)
    last_name = _D.Column(_D.String(20), nullable=False)
    phone_main = _D.Column(_D.Integer, nullable=False)
    phone_alt = _D.Column(_D.Integer)
    email = _D.Column(_D.String(120), unique=True, nullable=False)
    profile_pic = _D.Column(_D.String(20), nullable=False, default='pic.jpg')
    date_added = _D.Column(_D.String(20), nullable=False, default=datetime.today().strftime('%Y-%m-%d'))
    password = _D.Column(_D.String(60), nullable=False)
    status = _D.Column(_D.String(10), nullable=False, default='active')
    is_driver = _D.Column(_D.String(5), nullable=False, default='no')
    is_admin = _D.Column(_D.String(5), nullable=False, default='no')
    work_schedule = _D.relationship('Schedule', backref='empid', lazy=True, foreign_keys='Schedule.emp_id')
    request_off = _D.relationship('Requests', backref='requestedby', lazy=True, foreign_keys='Requests.requested_by')
    available = _D.relationship('Available', backref='empid', lazy=True)
    schedules = _D.relationship('Schedule', backref='addedby', lazy=True, foreign_keys='Schedule.added_by')
    approvals = _D.relationship('Requests', backref='reviewby', lazy=True, foreign_keys='Requests.review_by')

    def __repr__(self):
        label_guy = self.first_name
        guy = Employee.query.filter_by(first_name=self.first_name)
        count_guy = 0
        for x in guy:
            count_guy += 1
        if count_guy > 1:
            for y in guy:
                if y.last_name[0] == self.last_name[0] and y.id != self.id:
                    count_guy = 99
                    break
            if count_guy == 99:
                label_guy = (label_guy + ' ' + self.last_name)
            else:
                label_guy = (label_guy + ' ' + self.last_name[0])
        return f"[GUY{self.id}] :: {label_guy}"

class Schedule(_D.Model):
    id = _D.Column(_D.Integer, primary_key=True)
    date_added = _D.Column(_D.String(20), nullable=False, default=datetime.today().strftime('%Y-%m-%d'))
    added_by = _D.Column(_D.Integer, _D.ForeignKey('employee.id'), nullable=False)
    work_date = _D.Column(_D.Integer, _D.ForeignKey('the_days.id'), nullable=False)
    emp_id = _D.Column(_D.Integer, _D.ForeignKey('employee.id'), nullable=False)
    on_off = _D.Column(_D.String(5), nullable=False, default='ON')
    start_time = _D.Column(_D.String(5), default='TBD')
    end_time = _D.Column(_D.String(5))

    def __repr__(self):
        day = TheDays.query.filter_by(id=self.work_date).first()
        guy = Employee.query.filter_by(id=self.emp_id).first()
        if self.on_off == 'ON':
            on = 'working'
        else:
            on = self.on_off
        label_guy = (guy.first_name + ' ' + guy.last_name)
        label_day = (day.day_name + ' ' + utils.month_num_to_abr(day.calid.the_month) + ' ' + str(day.day_num) + ', ' + str(day.calid.the_year))
        return f"[WORK{self.id}] :: {label_guy} is {on} on {label_day}"

class Requests(_D.Model):
    id = _D.Column(_D.Integer, primary_key=True)
    date_added = _D.Column(_D.String(20), nullable=False)
    requested_by = _D.Column(_D.Integer, _D.ForeignKey('employee.id'), nullable=False)
    # requested_date = _D.Column(_D.String(20), nullable=False)
    requested_date = _D.Column(_D.Integer, _D.ForeignKey('the_days.id'), nullable=False)
    requested_time = _D.Column(_D.String(20), nullable=False, default='All day')
    status = _D.Column(_D.String(10), nullable=False, default='pending')
    review_date = _D.Column(_D.String(20))
    review_by = _D.Column(_D.Integer, _D.ForeignKey('employee.id'))

class Available(_D.Model):
    id = _D.Column(_D.Integer, primary_key=True)
    emp_id = _D.Column(_D.Integer, _D.ForeignKey('employee.id'), nullable=False)
    monday = _D.Column(_D.String(20), nullable=False, default='1')
    tuesday = _D.Column(_D.String(20), nullable=False, default='1')
    wednesday = _D.Column(_D.String(20), nullable=False, default='1')
    thursday = _D.Column(_D.String(20), nullable=False, default='1')
    friday = _D.Column(_D.String(20), nullable=False, default='1')
    saturday = _D.Column(_D.String(20), nullable=False, default='1')
    sunday = _D.Column(_D.String(20), nullable=False, default='1')
    return_date = _D.Column(_D.String(20))
    leave_date = _D.Column(_D.String(20))

    def __repr__(self):
        return f'[AVAIL//GUY{self.emp_id}] :: M -> {self.monday} | Tu -> {self.tuesday} | W -> {self.wednesday} | Th -> {self.thursday} | F -> {self.friday} | Sa -> {self.saturday} | Su -> {self.sunday}'

class Event(_D.Model):
    id = _D.Column(_D.Integer, primary_key=True)
    date_added = _D.Column(_D.String(20), nullable=False)
    added_by = _D.Column(_D.Integer, _D.ForeignKey('employee.id'), nullable=False)
    # event_date = _D.Column(_D.String(20), nullable=False)
    event_date = _D.Column(_D.Integer, _D.ForeignKey('the_days.id'), nullable=False)
    event_name = _D.Column(_D.String(30), nullable=False)
    event_desc = _D.Column(_D.String(350), nullable=False, default='No description added yet.')
    # setup_date = _D.Column(_D.String(20), nullable=False, default='TBD')
    # pickup_date = _D.Column(_D.String(20), nullable=False, default='TBD')
    setup_date = _D.Column(_D.Integer, _D.ForeignKey('the_days.id'))
    pickup_date = _D.Column(_D.Integer, _D.ForeignKey('the_days.id'))
    after_hours_setup = _D.Column(_D.String(5))
    after_hours_pickup = _D.Column(_D.String(5))

class TheCalendar(_D.Model):
    id = _D.Column(_D.Integer, primary_key=True)
    the_month = _D.Column(_D.Integer, nullable=False)
    the_year = _D.Column(_D.Integer, nullable=False)
    num_days = _D.Column(_D.Integer, nullable=False)
    start_with = _D.Column(_D.String(10), nullable=False)
    the_days = _D.relationship('TheDays', backref='calid', lazy=True)

    def __repr__(self):
        mon = utils.month_num_to_str(self.the_month)
        return f"[CALENDAR{self.id}] :: {mon} {self.the_year}"


class TheDays(_D.Model):
    id = _D.Column(_D.Integer, primary_key=True)
    cal_id = _D.Column(_D.Integer, _D.ForeignKey('the_calendar.id'), nullable=False)
    day_name = _D.Column(_D.String(10), nullable=False)
    day_num = _D.Column(_D.Integer, nullable=False)
    schedule = _D.relationship('Schedule', backref='workdate', lazy=True)
    requests = _D.relationship('Requests', backref='requesteddate', lazy=True)
    events = _D.relationship('Event', backref='eventdate', lazy=True, foreign_keys='Event.event_date')
    event_setup = _D.relationship('Event', backref='setupdate', lazy=True, foreign_keys='Event.setup_date')
    event_pickup = _D.relationship('Event', backref='pickupdate', lazy=True, foreign_keys='Event.pickup_date')

    def __repr__(self):
        cal = TheCalendar.query.filter_by(id=self.cal_id).first()
        mon = utils.month_num_to_abr(cal.the_month)
        return f"[DAY{self.id}] :: {self.day_name}, {mon} {self.day_num}, {cal.the_year}"

_X.add_view(ModelView(Employee, _D.session))
_X.add_view(ModelView(Schedule, _D.session))
_X.add_view(ModelView(Requests, _D.session))
_X.add_view(ModelView(Available, _D.session))
_X.add_view(ModelView(Event, _D.session))
_X.add_view(ModelView(TheCalendar, _D.session))
_X.add_view(ModelView(TheDays, _D.session))
