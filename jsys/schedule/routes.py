from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule
from jsys.schedule.forms import AddWorkForm
from flask_login import current_user
from jsys import _D, utils, dataf
from datetime import datetime
import pickle

work = Blueprint('work', __name__)

@work.route('/schedule/add', methods=['GET', 'POST'])
def add_single():
    x = dataf.form_choices_active_emp()
    ### Employee drop down menu
    active_workers = Employee.query.filter_by(status='active')
    list_workers = [('','--- Select Employee ---')]
    for x in active_workers:
        list_workers.append((x.id, x.first_name + ' ' + x.last_name))
    ### Month and Year drop down menu - only current and beyond is choosable
    day, mon, yr = datetime.today().strftime('%d'), datetime.today().strftime('%m'), datetime.today().strftime('%Y')
    mon, yr = int(mon), int(yr)
    current_month = TheCalendar.query.filter_by(the_year=yr, the_month=mon).first()
    future_months = TheCalendar.query.filter(TheCalendar.id>=current_month.id).all()
    list_month_year = []
    for y in future_months:
        new_month = utils.month_num_to_str(y.the_month)
        new_year = utils.year_two_digits(y.the_year)
        list_month_year.append((y.id, new_month + ' ' + new_year))
    ### Build form and load dropdown choices
    form = AddWorkForm()
    form.worker.choices = list_workers
    form.month_year_opt.choices = list_month_year[0:6]
    ### Form submit handling
    if form.validate_on_submit():
        kill = 'live'
        try:
            int(form.worker.data)
            print('This sure is an integer', form.worker.data)
        except:
            flash(f'Invalid Employee Selection')
            print('That ain\'t no integer', form.worker.data)
            kill = 'die'
        try:
            x = int(form.day_field.data)
            print('This sure is an integer', form.day_field.data)
            if x < 1 or x > 31:
                flash(f'Day must be between 1 and 31: not \'{form.day_field.data}\'')
                kill = 'die'
        except:
            flash(f'The day must be a number: not \'{form.day_field.data}\'')
            print('That ain\'t no integer', form.day_field.data)
            kill = 'die'
        print(kill)
        if kill == 'die':
            return redirect(url_for('work.add_single'))
        else:
            print(form.data)
            guy = Employee.query.filter_by(id=form.worker.data).first()
            d = TheDays.query.filter_by(cal_id=form.month_year_opt.data,day_num=x).first()
            schedule = Schedule(added_by=current_user.id, work_date=d.id, emp_id=guy.id, on_off=form.work_status.data)
            _D.session.add(schedule)
            print(schedule)
            _D.session.commit()
            flash(f'Added entry for {guy.first_name} {guy.last_name}')
        return redirect(url_for('main.home'))


    return render_template('add_work_single.html', form=form, title='Add Schedule Entry')
