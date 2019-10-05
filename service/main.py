from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
import os
from .config import SETTINGS
FLASK_ENV = os.environ.get('FLASK_ENV')

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
marshmallow = Marshmallow()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    return app

app = create_app(SETTINGS.get(FLASK_ENV, 'default'))
db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
marshmallow.init_app(app)

from . import models

admin.add_view(ModelView(models.OrgClient, db.session))
admin.add_view(ModelView(models.OrgSector, db.session))
admin.add_view(ModelView(models.OrgPerson, db.session))
admin.add_view(ModelView(models.OrgTeam, db.session))

from .api.resources import OrgClientResource
from .api import api_bp

api = Api(api_bp)
api.add_resource(OrgClientResource, '/clients')

app.register_blueprint(api_bp, url_prefix='/api')

