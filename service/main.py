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
marsh = Marshmallow()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    return app

app = create_app(SETTINGS.get(FLASK_ENV, 'default'))
db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
marsh.init_app(app)

from . import models

admin.add_view(ModelView(models.OrgClient, db.session))
admin.add_view(ModelView(models.OrgSector, db.session))
admin.add_view(ModelView(models.OrgPerson, db.session))
admin.add_view(ModelView(models.OrgTeam, db.session))

from .api.resources import (OrgClientResource, OrgClientListResource,
                            OrgSectorResource, OrgSectorListResource,
                            OrgPersonResource, OrgPersonListResource,
                            OrgTeamResource, OrgTeamListResource,
                            DatasetResource, DatasetListResource,
                            DataSchemaResource, DataSchemaListResource,
                            DataRequestResource, DataRequestListResource,
                            )
from .api import api_bp

api = Api(api_bp)
api.add_resource(OrgClientListResource, '/clients')
api.add_resource(OrgClientResource, '/clients/<int:id>')
api.add_resource(OrgSectorListResource, '/sectors')
api.add_resource(OrgSectorResource, '/sectors/<int:id>')
api.add_resource(OrgPersonListResource, '/persons')
api.add_resource(OrgPersonResource, '/persons/<int:id>')
api.add_resource(OrgTeamListResource, '/teams')
api.add_resource(OrgTeamResource, '/teams/<int:id>')
api.add_resource(DatasetListResource, '/datasets')
api.add_resource(DatasetResource, '/datasets/<int:id>')
api.add_resource(DataSchemaListResource, '/schemas')
api.add_resource(DataSchemaResource, '/schemas/<int:id>')
api.add_resource(DataRequestListResource, '/requests')
api.add_resource(DataRequestResource, '/requests/<int:id>')

app.register_blueprint(api_bp, url_prefix='/api')

