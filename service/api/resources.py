from flask_restful import Resource
from service.main import db
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from service.models import (OrgClient, OrgClientSchema,
                                OrgSector, OrgSectorSchema,
                                OrgPerson, OrgPersonSchema,
                                OrgTeam, OrgTeamSchema,
                                Dataset, DatasetSchema,
                                DataSchemaSchema, DataSchema,
                                DataRequestSchema, DataRequest,
                                )

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
        errors = dataset_schema.validate(dataset_dict)
        if errors:
            return errors, 400
        user = OrgPerson.query.filter_by(email=dataset_dict['email']).first()
        if not user:
            return {'message': '{} not found.'.format(dataset_dict['email'])}
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


data_schema = DataSchemaSchema()
data_schemas = DataSchemaSchema(many=True)
class DataSchemaResource(Resource):
    def get(self, id):
        schema = DataSchema.query.get_or_404(id)
        return data_schema.dump(schema)


class DataSchemaListResource(Resource):
    def get(self):
        schema = DataSchema.query.all()
        return data_schemas.dump(schema)

    def post(self):
        schema_dict = request.get_json()
        if not schema_dict:
            return {'error': 'No input data provided.'}
        errors = data_schema.validate(schema_dict)
        if errors:
            return errors, 400
        user = OrgPerson.query.filter_by(email=schema_dict['email']).first()
        if not user:
            return {'message': '{} not found.'.format(schema_dict['email'])}

        dataset_id = schema_dict['dataset_id']
        dataset = Dataset.query.get_or_404(dataset_id)
        if not dataset:
            return {'error': 'Dataset with ID={} not found.'.format(dataset_id)}
        else:
            matched_fields = [(k,v) for k,v in schema_dict['schema'].items()
                                    if v in dataset.fields]
            if not matched_fields:
                return {'error': 'Schema does not match the dataset.'}

            schema = DataSchema(creator=user,
                                dataset=dataset,
                                schema=dict(matched_fields))
            try:
                db.session.add(schema)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}

        return jsonify(data_schema.dump(schema))


request_schema = DataRequestSchema()
requests_schema = DataRequestSchema(many=True)
class DataRequestResource(Resource):
    def get(self, id):
        request = DataRequest.query.get_or_404(id)
        return requests_schema.dump(request)


class DataRequestListResource(Resource):
    def get(self):
        requests = DataRequest.query.all()
        return requests_schema.dump(requests)


    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            return {'message': 'No input data provided.'}, 400

        errors = request_schema.validate(request_dict)
        if errors:
            return errors, 400

        email = request_dict.get('email')
        if email:
            user = OrgPerson.query.filter_by(email=email).first()
            if not user:
                return {'error': '{} not found.'}, 400
        else:
            return {'error': 'No email is provided.'}, 400

        dataset_id = request_dict.get('dataset_id')
        if dataset_id:
            dataset = Dataset.query.get(dataset_id)
            if not dataset:
                return {'error': 'Dataset with ID={} not found.'\
                            .format(dataset_id)}
            req = DataRequest(creator=user,
                                endpoint=request_dict['endpoint'],
                                dtype=request_dict['dtype'],
                                dataset=dataset)
            try:
                db.session.add(req)
                db.session.commit()
            except SQLAlchemyError as e:
                return {'error': str(e)}, 400

        return request_schema.dump(req)