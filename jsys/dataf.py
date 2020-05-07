from jsys.models import TheDays, TheCalendar, Employee
from jsys import _D, utils
from datetime import datetime

def form_choices_active_emp():
    list = [('', '--- Select Employee ---')]
    guy = Employee.query.filter_by(status='active')
    for x in guy:
        list.append((x.id, x.first_name + ' ' + x.last_name))
    return list

def form_choices_mon_yr():
    day, mon, yr = datetime.today().strftime('%d'), datetime.today().strftime('%m'), datetime.today().strftime('%Y')
    mon, yr = int(mon), int(yr)
    current_month = TheCalendar.query.filter_by(the_year=yr, the_month=mon).first()
    future_months = TheCalendar.query.filter(TheCalendar.id>=current_month.id).all()
    list_month_year = []
    for y in future_months:
        new_month = utils.month_num_to_str(y.the_month)
        new_year = utils.year_two_digits(y.the_year)
        list_month_year.append((y.id, new_month + ' ' + new_year))
    return list_month_year

def alpha_today(x,y):
    month = TheCalendar.query.filter_by(id=x).first()
    day = TheDays.query.filter(TheDays.day_num==y, TheDays.cal_id==month.id).first()
    return day

def today():
    now = datetime.now()
    this_month = TheCalendar.query.filter_by(the_year=now.year,the_month=int(now.month)).first()
    this_day = TheDays.query.filter_by(calid=this_month, day_num=now.day).first()
    return this_day
