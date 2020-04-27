from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule, Requests, Available
from jsys.people.forms import RegGuy, LoginForm, UpdateAvailabilityForm
from flask_login import login_user, current_user, logout_user, login_required
from jsys import _D, _E, _L, utils

guy = Blueprint('guy', __name__)

@guy.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You\'re already logged in!', 'danger')
        return redirect(url_for('main.home'))
    form = RegGuy()
    if form.validate_on_submit():
        hsh = _E.generate_password_hash(form.pw.data).decode('utf-8')
        guy = Employee(first_name=form.fname.data, last_name=form.lname.data, email=form.email.data, phone_main=form.num.data, password=hsh)
        _D.session.add(guy)
        _D.session.commit()
        flash(f'New account created.')
        return redirect(url_for('guy.login'))
    x = 'All fields are required.'
    return render_template('register.html', form=form, title='Register Your Employee Account', def_text=x)

@guy.route('/availability/update', methods=['GET', 'POST'])
def edit_avail():
    form = UpdateAvailabilityForm()
    if form.validate_on_submit():
        mon = form.monday_opt.choices[int(form.monday_opt.data)-1][1]
        tue = form.tuesday_opt.choices[int(form.tuesday_opt.data)-1][1]
        wed = form.wednesday_opt.choices[int(form.wednesday_opt.data)-1][1]
        thu = form.thursday_opt.choices[int(form.thursday_opt.data)-1][1]
        fri = form.friday_opt.choices[int(form.friday_opt.data)-1][1]
        sat = form.saturday_opt.choices[int(form.saturday_opt.data)-1][1]
        sun = form.sunday_opt.choices[int(form.sunday_opt.data)-1][1]
        hours = Available(emp_id=current_user.id, monday=mon, tuesday=tue, wednesday=wed, thursday=thu, friday=fri, saturday=sat, sunday=sun)
        #_D.session.add(hours)
        #_D.session.commit()
        flash(f'Availability Updated')
        print(hours)
        return redirect(url_for('guy.profile'))
    return render_template('update_availability.html', title='Update Availability', form=form)

@guy.route('/login', methods=['GET', 'POST'])
def login():
    ### FOR CHANGING PASSWORD ENCODING ON UPLOAD
    #temp = Employee.query
    #for x in temp:
    #    x.password = _E.generate_password_hash('1')
    #_D.session.commit()
    if current_user.is_authenticated:
        flash(f'You\'re already logged in!', 'danger')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        guy = Employee.query.filter_by(email=form.email.data).first()
        if guy and _E.check_password_hash(guy.password, form.pw.data):
            login_user(guy, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in as ' + guy.first_name + ' ' + guy.last_name)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('You don\'t belong here.', 'danger')
    x = False
    return render_template('login.html', title='Login To Continue', form=form, def_text=x)

@guy.route('/logout')
def logout():
    logout_user()
    flash(f'Logged out!')
    return redirect(url_for('main.home'))

@guy.route('/profile')
def profile():
    guy = Employee.query.filter_by(id=current_user.id).first()
    hours = Available.query.filter_by(emp_id=current_user.id).first()
    return render_template('view_profile.html', title='Profile', guy=guy, hours=hours, utils=utils)
