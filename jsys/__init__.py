import os
from flask import Flask, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin

_D = SQLAlchemy()
_E = Bcrypt()
_L = LoginManager()
_X = Admin()

def build():
    _A = Flask(__name__)

    _A.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///the.db'
    _A.config['SECRET_KEY'] = os.environ.get('SK')

    _D.init_app(_A)
    _E.init_app(_A)
    _L.init_app(_A)
    _X.init_app(_A)

    from jsys.main.routes import main
    _A.register_blueprint(main)
    from jsys.people.routes import guy
    _A.register_blueprint(guy)
    from jsys.calendar.routes import cal
    _A.register_blueprint(cal)
    from jsys.schedule.routes import work
    _A.register_blueprint(work)

    return _A
