from app.models import *
from db import session
from datetime import datetime
from sqlalchemy import text
from flask import request
from flask_login import LoginManager, UserMixin, login_required

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import marshal

datetype = lambda x: datetime.strptime(x, '%Y-%m-%d')
date_error_help = "Date fields should be entered as: YYYY-MM-DD"

class Date(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')

################ Marshalers ####################

child_fields = {
    'id': fields.Integer,
    'english_name': fields.String,
    'chinese_name': fields.String,
    'pinyin_name': fields.String,
    'nickname': fields.String,
    'sex': fields.String,
    'birth_date': Date,
    'abandonment_date': Date,
    'program_entry_date': Date,
    'program_departure_date': Date,
    'program_departure_reason': fields.String,
    'child_history': fields.String,
    'medical_history': fields.String,
    'uri': fields.Url('entity', absolute=True)
}


################ Parsers ####################

entity_names = ['child', 
                'childnote',
                'partner',      
                'caregiver',
                'specialist',
                'specialisttype',
                'milestonetypecategory',
                'milestonetype',
                'doctortype',
                'doctor',
                'measurementtype',
                'camp',
                'medicalcondition',
                'medication']



# Entity base parsers, from which all other entity parsers will derive
entity_parser_help = "Parameter entity_name must be provided! Legal values: " + ",".join(entity_names)
entity_parser_base = reqparse.RequestParser()
entity_parser_base.add_argument('entity_name', required=True, location='args', choices=entity_names, help=entity_parser_help)

# Parser for input date related to a child object.
child_parser = reqparse.RequestParser()
child_parser.add_argument('english_name', required=True)
child_parser.add_argument('chinese_name')
child_parser.add_argument('pinyin_name')
child_parser.add_argument('nickname')
child_parser.add_argument('sex', required=True)
child_parser.add_argument('birth_date', type=datetype, help=date_error_help)
child_parser.add_argument('abandonment_date', type=datetype, help=date_error_help)
child_parser.add_argument('program_entry_date', type=datetype, help=date_error_help)
child_parser.add_argument('program_departure_date', type=datetype, help=date_error_help)
child_parser.add_argument('program_departure_reason')
child_parser.add_argument('child_history')
child_parser.add_argument('medical_history')

# When updating a child, no argument is required
# so replace arguments fields from the original child_parser.
child_update_parser = child_parser.copy()
child_update_parser.replace_argument('english_name', required=False)
child_update_parser.replace_argument('sex', required=False)

################ Look Up Tables ###############

entity_create_parsers = {   'child': child_parser }

entity_update_parsers = {   'child': child_update_parser }

entity_marshallers = {      'child': child_fields }

entity_classes = {  'child': Child,
                    'childnote': ChildNote,
                    'partner': Partner,
                    'caregiver': Caregiver,
                    'specialist': Specialist,
                    'specialisttype': SpecialistType,
                    'milestonetypecategory': MilestoneTypeCategory,
                    'milestonetype': MilestoneType,
                    'doctortype': DoctorType,
                    'doctor': Doctor,
                    'measurementtype': MeasurementType,
                    'camp': Camp,
                    'medicalcondition': MedicalCondition,
                    'medication': Medication }

################ Resources ####################


# TODO: Refactor duplicate code in this resource class.
class EntityResource(Resource):
    def get(self, id):
        args = entity_parser_base.parse_args()
        entity_name = args['entity_name']
        entity_class = entity_classes[entity_name]
        marshaller = entity_marshallers[entity_name]
        entity = session.query(entity_class).filter(entity_class.id == id).first()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(entity_name, id))
        return marshal(entity, marshaller), 200

    def delete(self, id):
        args = entity_parser_base.parse_args()
        entity_name = args['entity_name']
        entity_class = entity_classes[entity_name]
        entity = session.query(entity_class).filter(entity_class.id == id).first()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(entity_name, id))
        session.delete(entity)
        session.commit()
        return {}, 204

    def put(self, id):
        args = entity_parser_base.parse_args()
        entity_name = args['entity_name']
        entity_class = entity_classes[entity_name]
        marshaller = entity_marshallers[entity_name]
        entity_parser = entity_update_parsers[entity_name]
        entity = session.query(entity_class).filter(entity_class.id == id).first()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(entity_name, id))
        entity_args = entity_parser.parse_args()
        raw_json = request.get_json()
        for key in entity_args.keys():
            # Only update keys that are sent in the Json body
            if key in raw_json.keys():
                setattr(entity, key, entity_args[key])
        
        session.add(entity)
        session.commit()
        return marshal(entity, marshaller), 201

class EntityListResource(Resource):
    def get(self):
        args = entity_parser_base.parse_args()
        entity_name = args['entity_name']
        entity_class = entity_classes[entity_name]
        marshaller = entity_marshallers[entity_name]
        entities = session.query(entity_class).all()
        return marshal(entities, marshaller), 200

    def post(self):
        args = entity_parser_base.parse_args()
        entity_name = args['entity_name']
        entity_class = entity_classes[entity_name]
        marshaller = entity_marshallers[entity_name]
        entity_parser = entity_create_parsers[entity_name]
        entity_args = entity_parser.parse_args()
        entity = entity_class()
        for key in entity_args.keys():
            setattr(entity, key, entity_args[key])
        session.add(entity)
        session.commit()
        return marshal(entity, marshaller), 201

# Deprecated... to be deleted

#class ChildResource(Resource):
#    def get(self, id):
#        child = session.query(Child).filter(Child.id == id).first()
#        if not child:
#            abort(404, message="Child {} doesn't exist".format(id))
#        return marshal(child, child_fields), 200
#
#    def delete(self, id):
#        child = session.query(Child).filter(Child.id == id).first()
#        if not child:
#            abort(404, message="Child {} doesn't exist".format(id))
#        session.delete(child)
#        session.commit()
#        return {}, 204
#
#    @marshal_with(child_fields)
#    def put(self, id):
#        args = child_update_parser.parse_args()
#        child = session.query(Child).filter(Child.id == id).first()
#        if not child:
#            abort(404, message="Child {} doesn't exist".format(id))
#        for key in args.keys():
#            setattr(child, key, args[key])
#        
#        session.add(child)
#        session.commit()
#        return child, 201
#    
#    
#class ChildListResource(Resource):
#    @marshal_with(child_fields)
#    def get(self):
#        children = session.query(Child).all()
#        return children, 200
#
#    @marshal_with(child_fields)
#    def post(self):
#        args = child_parser.parse_args()
#        child = Child()
#        for key in args.keys():
#            setattr(child, key, args[key])
#        session.add(child)
#        session.commit()
#        return child, 201


query_parser = reqparse.RequestParser()
query_parser.add_argument('query', required=True)

# A generic SQL query API
class QueryResource(Resource):
    def post(self):
        args = query_parser.parse_args()
        query = args['query']
        if not query.lower().startswith("select"):
            abort(400, message="The query API endpoint is for 'Select' queries only!")
        if ";" in query:
            abort(400, message="Query messages must not contain semicolons!")
        sql = text(query)
        result = session.execute(sql)
        result_dict = []
        for row in result:
            result_dict.append(dict(zip(row.keys(), row)))
        return result_dict, 200
 
# Resource for calling a session.rollback()
class RollbackResource(Resource):
    def post(self):
        session.rollback();
        response = { 'message': 'Successfully rolled back the session!' }
        return response, 200

# Resource for checking online status
class HeartbeatResource(Resource):
    decorators = [login_required]
    def get(self):
        response = { 'message': 'beat' }
        return response, 200

