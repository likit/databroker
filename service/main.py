from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from .config import SETTINGS

FLASK_ENV = os.environ.get('FLASK_ENV')

db = SQLAlchemy()
ma = Migrate()
admin = Admin()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    return app

app = create_app(SETTINGS.get(FLASK_ENV, 'default'))
db.init_app(app)
ma.init_app(app, db)
admin.init_app(app)

from . import models

admin.add_view(ModelView(models.OrgClient, db.session))
admin.add_view(ModelView(models.OrgSector, db.session))
admin.add_view(ModelView(models.OrgPerson, db.session))
admin.add_view(ModelView(models.OrgTeam, db.session))


@app.route('/')
def hello():
    return '<h1>Hello, World</h1>'