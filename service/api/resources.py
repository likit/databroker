from flask_restful import Resource
from service.models import (OrgClient, OrgClientSchema,
                                OrgSector, OrgSectorSchema,
                                OrgPerson, OrgPersonSchema)

org_client_schema = OrgClientSchema()
org_clients_schema = OrgClientSchema(many=True)

class OrgClientResource(Resource):
    def get(self):
        clients = OrgClient.query.all()
        return org_clients_schema.dump(clients)


org_sector_schema = OrgSectorSchema()
org_sectors_schema = OrgSectorSchema(many=True)
class OrgSectorResource(Resource):
    def get(self):
        sectors = OrgSector.query.all()
        return org_sectors_schema.dump(sectors)


org_person_schema = OrgPersonSchema()
org_persons_schema = OrgPersonSchema(many=True)
class OrgPersonResource(Resource):
    def get(self):
        persons = OrgPerson.query.all()
        return org_persons_schema.dump(persons)