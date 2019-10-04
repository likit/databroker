from .main import db


class OrgClient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('org_sector.id'))
    sector = db.relationship('OrgSector', backref=db.backref('organizations',
                                lazy='dynamic', order_by='OrgClient.name'))


class OrgSector(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sector = db.Column(db.String(255), nullable=False)