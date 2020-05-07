from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule
from jsys.schedule.forms import AddWorkForm, RequestOffForm
from flask_login import current_user
from jsys import _D, utils, dataf
from datetime import datetime
import pickle

work = Blueprint('work', __name__)

@work.route('/request-off', methods=['GET', 'POST'])
def req_off():
    list_month_year = dataf.form_choices_mon_yr()
    form = RequestOffForm()
    form.month_year_opt.choices = list_month_year[0:10]
    if form.validate_on_submit():
        print(form.month_year_opt.data)
        flash(f'added?')
        return redirect(url_for('work.req_off'))
    return render_template('request_off.html', title='Request Off', form=form)


@work.route('/schedule')
def sched():
    if current_user.is_authenticated:
        this_day = dataf.today()
        work_this = Schedule.query.filter_by(emp_id=current_user.id).filter(Schedule.work_date>=this_day.id, Schedule.work_date<=this_day.id+6).order_by(Schedule.work_date).all()
        work_next = Schedule.query.filter_by(emp_id=current_user.id).filter(Schedule.work_date>=this_day.id+7, Schedule.work_date<=this_day.id+13).order_by(Schedule.work_date).all()
    else:
        flash(f'Restricted area. Please login below.')
        return redirect(url_for('guy.login'))
    return render_template('view_schedule.html', title='Schedule', work=work_this, work2=work_next, utils=utils)


@work.route('/schedule/add', methods=['GET', 'POST'])
def add_single():
    list_workers = dataf.form_choices_active_emp()
    list_month_year = dataf.form_choices_mon_yr()
    form = AddWorkForm()
    form.worker.choices = list_workers
    form.month_year_opt.choices = list_month_year[0:6]
    ### Form submit handling
    if form.validate_on_submit():
        kill = 'live'
        try:
            int(form.worker.data)
        except:
            flash(f'Invalid Employee Selection')
            kill = 'die'
        try:
            x = int(form.day_field.data)
            if x < 1 or x > 31:
                flash(f'Day must be between 1 and 31: not \'{form.day_field.data}\'')
                kill = 'die'
        except:
            flash(f'The day must be a number: not \'{form.day_field.data}\'')
            kill = 'die'
        print(kill)
        if kill == 'die':
            return redirect(url_for('work.add_single'))
        else:
            guy = Employee.query.filter_by(id=form.worker.data).first()
            d = TheDays.query.filter_by(cal_id=form.month_year_opt.data,day_num=x).first()
            schedule = Schedule(added_by=current_user.id, work_date=d.id, emp_id=guy.id, on_off=form.work_status.data)
            _D.session.add(schedule)
            _D.session.commit()
            flash(f'Added entry for {guy.first_name} {guy.last_name}')
            return redirect(url_for('main.home'))
    return render_template('add_work_single.html', form=form, title='Add Schedule Entry')
