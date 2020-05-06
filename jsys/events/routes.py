from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule, Requests, Available
from jsys.events.forms import AddEventForm
from flask_login import login_user, current_user, logout_user, login_required
from jsys import _D, utils, dataf

job = Blueprint('job', __name__)

@job.route('/events')
def events():
    return render_template('view_events.html', title='Upcoming Events')

@job.route('/event/add', methods=['POST','GET'])
def add_event():
    list_month_year = dataf.form_choices_mon_yr()
    form = AddEventForm()
    form.event_my_opt.choices = list_month_year[0:12]
    form.setup_my_opt.choices = list_month_year[0:12]
    form.pickup_my_opt.choices = list_month_year[0:12]
    if form.validate_on_submit():
        print(form.event_day.data, form.event_my_opt.data)
        print(form.event_name.data, form.event_desc.data)
        print(form.setup_my_opt.data, form.setup_day.data, form.odd_setup.data)
        print(form.pickup_my_opt.data, form.pickup_day.data, form.odd_pickup.data)
        flash(f'Go!')
        return redirect(url_for('main.home'))
    return render_template('add_event.html', title='Add Event', form=form)

@job.route('/event/update', methods=['POST','GET'])
def update_event():
    form = AddEventForm()
    form.event_my_opt.choices = [(1,1)]
    #form.submit.label = '<label for="submit">Update</label>'
    if form.validate_on_submit():
        print('Mmoo0ooo')
    elif request.method == 'GET':
        form.event_name.data = 'YOOOOOOOOO'
        print('zoommmmM')
    return render_template('add_event.html', title='Add Event', form=form)
