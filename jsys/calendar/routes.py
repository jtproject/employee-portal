from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays
from jsys import _D, utils

cal = Blueprint('cal', __name__)

@cal.route('/create-days', methods=['GET'])
def create_days():
    cal = TheCalendar.query.all()
    #for x in cal:
    #    print(x.the_month)
    #    x.the_month = utils.month_num_to_abr(x.the_month)
    #    print(x.the_month)
    for x in cal:
        print('jsys.BUILD -> ' + utils.month_num_to_abr(x.the_month), x.the_year)
        count = 1
        weekday = x.start_with
        if x.the_days:
            day = TheDays.query.filter_by(cal_id=x.id).all()
            print('Data already exits :: ' + str(day[0].day_num) + '-' + str(day[-1].day_num))
        else:
            while count <= x.num_days:
                create = TheDays(cal_id=x.id, day_name=weekday, day_num=count)
                _D.session.add(create)
                print('jsys.ADDING -> ' + utils.weekday_str_to_abr(create.day_name) + ',', utils.month_num_to_abr(x.the_month), str(create.day_num) +',',  x.the_year)
                count += 1
                weekday = utils.weekday_next(weekday)
            count -= 1
            flash(f'Added {count} days to {utils.month_num_to_abr(x.the_month)} {utils.year_two_digits(x.the_year)}')
    _D.session.commit()
    day = TheDays.query.filter_by(cal_id=cal[-1].id).all()
    d = day[0]
    print(d)
    month = utils.month_num_to_str(d.calid.the_month)
    year = d.calid.the_year
    skip = utils.weekday_start(d.calid.start_with)
    count = 0
    while count < skip:
        x = TheDays(day_num='')
        day.insert(0, x)
        count += 1
    return render_template('view_cal_by_month.html', day=day, month=month, year=year, title='Calendar Overview')


@cal.route('/calendar/month')
def view_cal():
    day = TheDays.query.filter_by(cal_id=3).all()
    d = day[0]
    month = utils.month_num_to_str(d.calid.the_month)
    year = d.calid.the_year
    skip = utils.weekday_start(d.calid.start_with)
    count = 0
    while count < skip:
        x = TheDays(day_num='')
        day.insert(0, x)
        count += 1
    return render_template('view_cal_by_month.html', day=day, month=month, year=year, title='Calendar Overview')
