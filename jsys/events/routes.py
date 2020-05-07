from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule, Requests, Available, Event
from jsys.events.forms import AddEventForm
from flask_login import login_user, current_user, logout_user, login_required
from jsys import _D, utils, dataf
from datetime import datetime

job = Blueprint('job', __name__)

@job.route('/events')
def events():
    now = datetime.now()
    #today = dataf.today(int(now.day))
    job = Event.query
    job2 = Event.query
    return render_template('view_events.html', title='Upcoming Events', job=job, job2=job2, utils=utils)

@job.route('/event/add', methods=['POST','GET'])
def add_event():
    list_month_year = dataf.form_choices_mon_yr()
    form = AddEventForm()
    form.event_my_opt.choices = list_month_year[0:12]
    form.setup_my_opt.choices = list_month_year[0:12]
    form.pickup_my_opt.choices = list_month_year[0:12]
    if form.validate_on_submit():
        e_day = dataf.alpha_today(int(form.event_my_opt.data),int(form.event_day.data))
        x = Event(added_by=current_user.id, event_date=e_day, event_name=form.event_name.data, event_desc=form.event_desc.data)
        #_D.session.add(x)
        #_D.session.commit()
        print(x.event_date)
        flash(f'{form.event_name.data} event added.')
        return redirect(url_for('main.home'))
    return render_template('add_event.html', title='Add Event', form=form)

@job.route('/event/update/<int:event_id>', methods=['POST','GET'])
def update_event(event_id):
    job = Event.query.filter_by(id=event_id).first()
    list_month_year = dataf.form_choices_mon_yr()
    form = AddEventForm()
    form.event_my_opt.choices = list_month_year[0:12]
    form.setup_my_opt.choices = list_month_year[0:12]
    form.pickup_my_opt.choices = list_month_year[0:12]
    form.submit = form.submit2
    if form.validate_on_submit():
        job.event_desc = form.event_desc.data
        _D.session.commit()
        flash(f'{job.event_name} event ({utils.month_num_to_abr(job.eventdate.calid.the_month)} {job.eventdate.day_num}, {job.eventdate.calid.the_year}) updated')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.event_name.data = job.event_name
        form.event_my_opt.data = job.eventdate.calid.id
        form.event_day.data = job.eventdate.day_num
        form.event_desc.data = job.event_desc
    return render_template('add_event.html', title='Add Event', form=form)
