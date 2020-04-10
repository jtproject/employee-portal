from flask import render_template, url_for, request, Blueprint, redirect, flash
from jsys.models import TheCalendar, TheDays, Employee, Schedule, Requests, Available
from jsys.people.forms import RegGuy, LoginForm
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

@guy.route('/login', methods=['GET', 'POST'])
def login():
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
