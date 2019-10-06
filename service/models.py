from .main import db, marshmallow
from sqlalchemy.sql import func
from marshmallow import fields, Schema


class OrgClient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('org_sector.id'))
    sector = db.relationship('OrgSector', backref=db.backref('organizations',
                                lazy='dynamic', order_by='OrgClient.name'))

    teams = db.relationship('OrgTeam', secondary='org_client_team')

    def __str__(self):
        return u'{}:{}'.format(self.id, self.name)

class OrgSector(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sector = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return u'{}:{}'.format(self.id, self.sector)


class OrgPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname_th = db.Column(db.String(255))
    lastname_th = db.Column(db.String(255))
    firstname_en = db.Column(db.String(255), nullable=False)
    lastname_en = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('org_client.id'))
    organization = db.relationship('OrgClient',
                        backref=db.backref('persons', lazy='dynamic'))

    def __str__(self):
        return u'{}:{}'.format(self.id, self.email)


class OrgTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    active = db.Column(db.Boolean(), default=False)
    orgs = db.relationship('OrgClient', secondary='org_client_team')

    def __str__(self):
        return u'{}:{}'.format(self.id, self.name)

class OrgClientTeam(db.Model):
    __tablename__ = 'org_client_team'
    org_id = db.Column(db.Integer, db.ForeignKey('org_client.id'),
                        primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('org_team.id'),
                        primary_key=True)
    org = db.relationship('OrgClient', backref=db.backref('team_assoc'))
    team = db.relationship('OrgTeam', backref=db.backref('org_assoc'))


class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=True)
    fields = db.Column(db.JSON, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('org_person.id'))
    creator = db.relationship('OrgPerson', backref=db.backref('datasets'))


class DataSchema(db.Model):
    __tablename__ = 'data_schema'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                            onupdate=func.now())
    schema = db.Column(db.JSON, nullable=False)
    creator_id = db.Column(db.Integer,
                            db.ForeignKey('org_person.id', ondelete='CASCADE'))
    creator = db.relationship('OrgPerson', backref=db.backref('schemas'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    dataset = db.relationship('Dataset',
                                backref=db.backref('schemas', lazy='dynamic'))


class DataRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())
    creator_id = db.Column(db.Integer,
                            db.ForeignKey('org_person.id', ondelete='CASCADE'))
    creator = db.relationship('OrgPerson', backref=db.backref('requests'))
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    dataset = db.relationship('Dataset',
                                backref=db.backref('requests', lazy='dynamic'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'))
    destination = db.relationship('Destination',
                                    backref=db.backref('request', uselist=False))


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dest_type = db.Column(db.String(255), nullable=False)
    # Could be a Google Sheet ID, an API endpoint, etc.
    uri = db.Column(db.String(255), nullable=False)


class OrgClientSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    url = marshmallow.URLFor('api.orgclientresource',
                                id='<id>', _external=True)

    sector = fields.Nested('OrgSectorSchema', many=False)


class OrgSectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    sector = fields.String(required=True)
    url = marshmallow.URLFor('api.orgsectorresource',
                                id='<id>', _external=True)


class OrgPersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    org = fields.Nested('OrgClientSchema', many=False,
                        only=['id', 'name', 'url'])
    firstname_th = fields.String(required=False)
    lastname_th = fields.String(required=False)
    firstname_en = fields.String(required=True)
    lastname_en = fields.String(required=True)
    email = fields.String(required=True)
    url = marshmallow.URLFor('api.orgpersonresource',
                                id='<id>', _external=True)