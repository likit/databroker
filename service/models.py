from .main import db


class OrgClient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('org_sector.id'))
    sector = db.relationship('OrgSector', backref=db.backref('organizations',
                                lazy='dynamic', order_by='OrgClient.name'))

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
    firstname_en = db.Column(db.String(255))
    lastname_en = db.Column(db.String(255))
    email = db.Column(db.String(128))
    org_id = db.Column(db.Integer, db.ForeignKey('org_client.id'))
    organization = db.relationship('OrgClient',
                        backref=db.backref('persons', lazy='dynamic'))

    def __str__(self):
        return u'{}:{}'.format(self.id, self.email)