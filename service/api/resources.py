from flask_restful import Resource
from service.main import db
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from service.models import (OrgClient, OrgClientSchema,
                                OrgSector, OrgSectorSchema,
                                OrgPerson, OrgPersonSchema,
                                OrgTeam, OrgTeamSchema,
                                Dataset, DatasetSchema)

org_client_schema = OrgClientSchema()
org_clients_schema = OrgClientSchema(many=True)

class OrgClientListResource(Resource):
    def get(self):
        clients = OrgClient.query.all()
        return org_clients_schema.dump(clients)


class OrgClientResource(Resource):
    def get(self, id):
        client = OrgClient.query.get_or_404(id)
        return org_client_schema.dump(client)


org_sector_schema = OrgSectorSchema()
org_sectors_schema = OrgSectorSchema(many=True)
class OrgSectorResource(Resource):
    def get(self, id):
        sector = OrgSector.query.get_or_404(id)
        return org_sector_schema.dump(sector)


class OrgSectorListResource(Resource):
    def get(self):
        sectors = OrgSector.query.all()
        return org_sectors_schema.dump(sectors)


org_person_schema = OrgPersonSchema()
org_persons_schema = OrgPersonSchema(many=True)
class OrgPersonResource(Resource):
    def get(self, id):
        person = OrgPerson.query.get_or_404(id)
        return org_person_schema.dump(person)


class OrgPersonListResource(Resource):
    def get(self):
        persons = OrgPerson.query.all()
        return org_persons_schema.dump(persons)


org_team_schema = OrgTeamSchema()
org_teams_schema = OrgTeamSchema(many=True)
class OrgTeamResource(Resource):
    def get(self, id):
        team = OrgTeam.query.get_or_404(id)
        return org_team_schema.dump(team)


class OrgTeamListResource(Resource):
    def get(self):
        teams = OrgTeam.query.all()
        return org_teams_schema.dump(teams)


dataset_schema = DatasetSchema()
datasets_schema = DatasetSchema(many=True)
class DatasetResource(Resource):
    def get(self, id):
        dataset = Dataset.query.get_or_404(id)
        return dataset_schema.dump(dataset)


class DatasetListResource(Resource):
    def get(self):
        datasets = Dataset.query.all()
        return datasets_schema.dump(datasets)

    def post(self):
        dataset_dict = request.get_json()
        if not dataset_dict:
            return {'message': 'No input data provided.'}, 400
        existing_dataset = Dataset.query.filter_by(name=dataset_dict['name']).first()
        if existing_dataset:
            return {'message': 'Dataset named **{}** already exists.'\
                        .format(dataset_dict['name'])}, 400
        user = OrgPerson.query.filter_by(email=dataset_dict['email']).first()
        if not user:
            return {'message': '{} not found.'.format(dataset_dict['email'])}
        errors = dataset_schema.validate(dataset_dict)
        if errors:
            return errors, 400
        dataset = Dataset(name=dataset_dict['name'],
                            fields=dataset_dict['fields'],
                            creator=user)
        if 'description' in dataset_dict:
            dataset.description = dataset_dict['description']
        try:
            db.session.add(dataset)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, 400
        return dataset_schema.dump(dataset), 201