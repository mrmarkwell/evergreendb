from app.models import *
from db import session
from datetime import datetime
from sqlalchemy import text
from flask import request
from flask import jsonify
import json

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

################ Marshallers ####################

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
}

child_note_fields = {
    'id': fields.Integer,
    'date': Date,
    'note': fields.String,
    'flag': fields.Boolean,
    'child': fields.Integer,
}

partner_fields = {
    'id': fields.Integer,
    'english_name': fields.String,
    'chinese_name': fields.String,
    'pinyin_name': fields.String,
    'email': fields.String,
    'phone': fields.String
}

caregiver_fields = {
    'id': fields.Integer,
    'english_name': fields.String,
    'chinese_name': fields.String,
    'pinyin_name': fields.String,
}

child_partner_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'note': fields.String,
    'flag': fields.Boolean,
    'child_id': fields.Integer,
    'partner_id': fields.Integer
}


################ Parsers ####################

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

# child_note
child_note_parser = reqparse.RequestParser()
child_note_parser.add_argument('date', type=datetype, help=date_error_help)
child_note_parser.add_argument('note', required=True)
child_note_parser.add_argument('flag')
child_note_parser.add_argument('child', required=True)

child_note_update_parser = child_note_parser.copy()
child_note_update_parser.replace_argument('note', required=False)
child_note_update_parser.replace_argument('child', required=False)

# partner
partner_parser = reqparse.RequestParser()
partner_parser.add_argument('english_name', required=True)
partner_parser.add_argument('chinese_name')
partner_parser.add_argument('pinyin_name')
partner_parser.add_argument('email')
partner_parser.add_argument('phone')

partner_update_parser = partner_parser.copy()
partner_update_parser.replace_argument('english_name', required=False)

# caregiver
caregiver_parser = reqparse.RequestParser()
caregiver_parser.add_argument('english_name', required=True)
caregiver_parser.add_argument('chinese_name')
caregiver_parser.add_argument('pinyin_name')

caregiver_update_parser = caregiver_parser.copy()
caregiver_update_parser.replace_argument('english_name', required=False)

# try out id's with association tabls

child_partner_parser = reqparse.RequestParser()
child_partner_parser.add_argument('start_date', type=datetype, help=date_error_help)
child_partner_parser.add_argument('end_date', type=datetype, help=date_error_help)
child_partner_parser.add_argument('note')
child_partner_parser.add_argument('flag')
child_partner_parser.add_argument('child_id', required=True)
child_partner_parser.add_argument('partner_id', required=True)

child_partner_update_parser = child_partner_parser.copy()
child_partner_update_parser.replace_argument('child_id', required=False)
child_partner_update_parser.replace_argument('partner_id', required=False)
################ Look Up Tables ###############

class EntityData:
    def __init__(self, class_type, marshaller, create_parser, update_parser):
        self.class_type = class_type
        self.marshaller = marshaller
        self.create_parser = create_parser
        self.update_parser = update_parser

entity_data = {
    'child'                 : EntityData(Child, child_fields, child_parser, child_update_parser),
    'child_note'             : EntityData(ChildNote, child_note_fields, child_note_parser, child_note_update_parser),
    'partner'               : EntityData(Partner, partner_fields, partner_parser, partner_update_parser),
    'caregiver'             : EntityData(Caregiver, caregiver_fields, caregiver_parser, caregiver_update_parser),
#    'specialist'            : EntityData(Specialist, specialist_fields, specialist_parser, specialist_update_parser),
#    'specialist_type'        : EntityData(SpecialistType, _fields, _parser, _update_parser),
#    'milestone_type_category' : EntityData(MilestoneTypeCategory, _fields, _parser, _update_parser),
#    'milestone_type'         : EntityData(MilestoneType, _fields, _parser, _update_parser),
#    'doctor_type'            : EntityData(DoctorType, _fields, _parser, _update_parser),
#    'doctor'                : EntityData(Doctor, _fields, _parser, _update_parser),
#    'measurement_type'       : EntityData(MeasurementType, _fields, _parser, _update_parser),
#    'camp'                  : EntityData(Camp, _fields, _parser, _update_parser),
#    'medical_condition'      : EntityData(MedicalCondition, _fields, _parser, _update_parser),
#    'medication'            : EntityData(Medication, _fields, _parser, _update_parser),
    'child_partner'          : EntityData(ChildPartner, child_partner_fields, child_partner_parser, child_partner_update_parser)
}

entity_names = entity_data.keys()

################ Resources ####################

# Base resource class for resource data.
class ResourceBase(Resource):
    def __init__(self):
        self.ed = None

    # Call this right away to populate the entity data object.
    def get_entity_data(self, name):
        if name not in entity_names:
            abort(404, message="Invalid entity name: " + name + " Legal entity names are: " + ", ".join(entity_names))
        self.ed = entity_data[name]
 
    # For operations that can only be performed on one entity, get that entity by id
    # Throw an error if 'id' was not specified in the request.
    def get_entity_by_id(self):
        id = request.args.to_dict().get("id", None)
        if not id:
            abort(404, message="This operation must be passed a specific entity ID!")
        entity = session.query(self.ed.class_type).filter(self.ed.class_type.id == id).first()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(entity_name, id))
        return entity


class EntityResource(ResourceBase):
    # GET to get instances by filter arguments (e.g. ?english_name=Bobby&sex=M).
    # No arguments returns all entities of that type.
    def get(self, entity_name):
        self.get_entity_data(entity_name)
        entity = session.query(self.ed.class_type).filter_by(**request.args.to_dict()).all()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(entity_name, request.args.to_dict()))
        return marshal(entity, self.ed.marshaller), 200

    # DELETE to delete a single entity instance
    def delete(self, entity_name):
        self.get_entity_data(entity_name)
        entity = self.get_entity_by_id()
        session.delete(entity)
        session.commit()
        return {}, 204

    # PUT to update a single entity instance
    def put(self, entity_name):
        self.get_entity_data(entity_name)
        entity = self.get_entity_by_id()
        entity_args = self.ed.update_parser.parse_args()
        raw_json = request.get_json()
        for key in entity_args.keys():
            # Only update keys that are sent in the Json body
            if key in raw_json.keys():
                setattr(entity, key, entity_args[key])
        session.add(entity)
        session.commit()
        return marshal(entity, self.ed.marshaller), 201

    # Post to create a new entity
    def post(self, entity_name):
        self.get_entity_data(entity_name)
        entity_args = self.ed.create_parser.parse_args()
        entity = self.ed.class_type()
        for key in entity_args.keys():
            setattr(entity, key, entity_args[key])
        session.add(entity)
        session.commit()
        return marshal(entity, self.ed.marshaller), 201


# Resource for getting valid entity names.
class EntityListResource(ResourceBase):
    def get(self):        
        response = { "entity_names": entity_names }
        return response, 200


query_parser = reqparse.RequestParser()
query_parser.add_argument('query', required=True)

# A generic SQL query API
class QueryResource(ResourceBase):
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
class RollbackResource(ResourceBase):
    def post(self):
        session.rollback();
        response = { 'message': 'Successfully rolled back the session!' }
        return response, 200

# Resource for checking online status
class HeartbeatResource(ResourceBase):
    def get(self):
        response = { 'message': 'beat' }
        return response, 200

