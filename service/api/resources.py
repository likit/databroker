from flask_restful import Resource
from service.models import OrgClient, OrgClientSchema

org_client_schema = OrgClientSchema()
org_clients_schema = OrgClientSchema(many=True)

class OrgClientResource(Resource):
    def get(self):
        clients = OrgClient.query.all()
        return org_clients_schema.dump(clients)