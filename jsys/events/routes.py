from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule, Requests, Available
from jsys.events.forms import AddEventForm
from flask_login import login_user, current_user, logout_user, login_required
from jsys import _D, utils, dataf

job = Blueprint('job', __name__)

@job.route('/events')
def events():
    return render_template('view_events.html', title='Upcoming Events')

@job.route('/event/add')
def add_event():
    list_month_year = dataf.form_choices_mon_yr()
    form = AddEventForm()
    form.month_year_opt.choices = list_month_year[0:12]
    return render_template('add_event.html', title='Add Event', form=form)
