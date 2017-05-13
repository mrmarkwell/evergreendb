from datetime import datetime
import json

from app.models import *
from db import session
from sqlalchemy import text
from sqlalchemy.sql.expression import and_
from flask import request
from flask import jsonify

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

base_fields = {
    'id': fields.Integer,
    'english_name': fields.String,
    'chinese_name': fields.String,
    'pinyin_name': fields.String,
    }
child_fields = base_fields.copy()
child_fields.update({
    'nickname': fields.String,
    'sex': fields.String,
    'birth_date': Date,
    'abandonment_date': Date,
    'program_entry_date': Date,
    'program_departure_date': Date,
    'program_departure_reason': fields.String,
    'child_history': fields.String,
    'medical_history': fields.String,
})
child_note_fields = {
    'id': fields.Integer,
    'date': Date,
    'note': fields.String,
    'flag': fields.Boolean,
    'child': fields.Integer,
}
partner_fields = base_fields.copy()
partner_fields.update({'email': fields.String, 'phone': fields.String })
caregiver_fields = base_fields.copy()
specialist_fields = base_fields.copy()
specialist_fields.update({'specialist_type': fields.Integer})
specialist_type_fields = base_fields.copy()
milestone_type_category_fields = base_fields.copy()
milestone_type_fields = base_fields.copy()
milestone_type_fields.update({'milestone_category': fields.String})
doctor_type_fields = base_fields.copy()
doctor_fields = {
    'id': fields.Integer,
    'doctor_english_name':   fields.String,
    'doctor_chinese_name':   fields.String,
    'doctor_pinyin_name':    fields.String,
    'facility_english_name': fields.String,
    'facility_chinese_name': fields.String,
    'facility_pinyin_name':  fields.String,
    'doctor_type': fields.Integer
    }
measurement_type_fields = base_fields.copy()
measurement_type_fields.update({'units': fields.String})

camp_fields = base_fields.copy()
medical_condition_fields = base_fields.copy()
medication_fields = base_fields.copy()
medication_fields.update({'milligram_dose': fields.Float})


child_partner_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'note': fields.String,
    'flag': fields.Boolean,
    'child_id': fields.Integer,
    'partner_id': fields.Integer
}

child_camp_fields = {
    'id': fields.Integer,
    'date': Date,
    'node': fields.String,
    'child_id': fields.Integer,
    'camp_id': fields.Integer
    }

child_assessment_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'note': fields.String,
    'flag': fields.Boolean,
    'specialist_id':fields.Integer
    }

child_caregiver_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'note': fields.String,
    'child_id': fields.Integer,
    'caregiver_id': fields.Integer
    }

child_measurement_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'value': fields.Float,
    'measurement_type_id': fields.Integer
    }

child_milestone_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'milestone_type_id': fields.Integer
    }

child_doctor_visit_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'note': fields.String,
    'doctor_id': fields.Integer
    }

child_medical_condition_fields = {
    'id': fields.Integer,
    'child_id': fields.Integer,
    'medical_condition_id': fields.Integer
    }

child_medication_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'child_id': fields.Integer,
    'medication_id': fields.Integer,
    'dosage1': fields.Float,
    'dosage2': fields.Float,
    'dosage3': fields.Float
    }

################ Parsers ####################

# A base entity parser for other parsers to derive from
base_parser = reqparse.RequestParser()
base_parser.add_argument('english_name', required=True)
base_parser.add_argument('chinese_name')
base_parser.add_argument('pinyin_name')

# Parser for input date related to a child object.
child_parser = base_parser.copy()
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
child_note_parser.add_argument('flag', type=bool)
child_note_parser.add_argument('child', required=True)

child_note_update_parser = child_note_parser.copy()
child_note_update_parser.replace_argument('note', required=False)
child_note_update_parser.replace_argument('child', required=False)

# partner
partner_parser = base_parser.copy()
partner_parser.add_argument('email')
partner_parser.add_argument('phone')

partner_update_parser = partner_parser.copy()
partner_update_parser.replace_argument('english_name', required=False)

# caregiver
caregiver_parser = base_parser.copy()

caregiver_update_parser = caregiver_parser.copy()
caregiver_update_parser.replace_argument('english_name', required=False)

# specialist

specialist_parser = base_parser.copy()
specialist_parser.add_argument('specialist_type', type=int, required=True)
specialist_update_parser = specialist_parser.copy()
for arg in specialist_update_parser.args:
    specialist_update_parser.replace_argument(arg, required=False)

# specialist_type

specialist_type_parser = base_parser.copy()
specialist_type_update_parser = specialist_type_parser.copy()
for arg in specialist_type_update_parser.args:
    specialist_type_update_parser.replace_argument(arg, required=False)

# milestone_type_category

milestone_type_category_parser = base_parser.copy()
milestone_type_category_update_parser = milestone_type_category_parser.copy()
for arg in milestone_type_category_update_parser.args:
    milestone_type_category_update_parser.replace_argument(arg, required=False)

# milestone_type

milestone_type_parser = base_parser.copy()
milestone_type_update_parser = milestone_type_parser.copy()
for arg in milestone_type_update_parser.args:
    milestone_type_update_parser.replace_argument(arg, required=False)

# doctor_type

doctor_type_parser = base_parser.copy()
doctor_type_update_parser = doctor_type_parser.copy()
for arg in doctor_type_update_parser.args:
    doctor_type_update_parser.replace_argument(arg, required=False)

# doctor

doctor_parser = reqparse.RequestParser()
doctor_parser.add_argument('doctor_english_name', required=True)
doctor_parser.add_argument('doctor_chinese_name')
doctor_parser.add_argument('doctor_pinyin_name')
doctor_parser.add_argument('facility_english_name')
doctor_parser.add_argument('facility_chinese_name')
doctor_parser.add_argument('facility_pinyin_name')
doctor_parser.add_argument('doctor_type', type=int, required=True)
doctor_update_parser = doctor_parser.copy()
for arg in doctor_update_parser.args:
    doctor_update_parser.replace_argument(arg, required=False)

# measurement_type

measurement_type_parser = base_parser.copy()
measurement_type_parser.add_argument('units', required=True)
measurement_type_update_parser = measurement_type_parser.copy()
for arg in measurement_type_update_parser.args:
    measurement_type_update_parser.replace_argument(arg, required=False)

# camp

camp_parser = base_parser.copy()
camp_update_parser = camp_parser.copy()
for arg in camp_update_parser.args:
    camp_update_parser.replace_argument(arg, required=False)

# medical_condition

medical_condition_parser = base_parser.copy()
medical_condition_update_parser = medical_condition_parser.copy()
for arg in medical_condition_update_parser.args:
    medical_condition_update_parser.replace_argument(arg, required=False)

# medication

medication_parser = base_parser.copy()
medication_parser.add_argument('milligram_dose', type=float, required=True)
medication_update_parser = medication_parser.copy()
for arg in medication_update_parser.args:
    medication_update_parser.replace_argument(arg, required=False)

# child_partner
child_partner_parser = reqparse.RequestParser()
child_partner_parser.add_argument('start_date', type=datetype, help=date_error_help)
child_partner_parser.add_argument('end_date', type=datetype, help=date_error_help)
child_partner_parser.add_argument('note')
child_partner_parser.add_argument('flag', type=bool)
child_partner_parser.add_argument('child_id', type=int, required=True)
child_partner_parser.add_argument('partner_id', type=int, required=True)

child_partner_update_parser = child_partner_parser.copy()
child_partner_update_parser.replace_argument('child_id', type=int, required=False)
child_partner_update_parser.replace_argument('partner_id', type=int, required=False)

# child_camp
child_camp_parser = reqparse.RequestParser()
child_camp_parser.add_argument('date', required=True, type=datetype, help=date_error_help)
child_camp_parser.add_argument('note')
child_camp_parser.add_argument('child_id', type=int, required=True)
child_camp_parser.add_argument('camp_id', type=int, required=True)

child_camp_update_parser = child_camp_parser.copy()
child_camp_update_parser.replace_argument('date', required=False, type=datetype, help=date_error_help)
child_camp_update_parser.replace_argument('child_id', type=int, required=False)
child_camp_update_parser.replace_argument('camp_id', type=int, required=False)

# child_assessment

child_assessment_parser = reqparse.RequestParser()
child_assessment_parser.add_argument('date', required=True, type=datetype, help=date_error_help)
child_assessment_parser.add_argument('note')
child_assessment_parser.add_argument('child_id', type=int, required=True)
child_assessment_parser.add_argument('flag', type=bool)
child_assessment_parser.add_argument('specialist_id', type=int, required=True)

child_assessment_update_parser = child_assessment_parser.copy()
child_assessment_update_parser.replace_argument('date', required=False, type=datetype, help=date_error_help)
child_assessment_update_parser.replace_argument('child_id', type=int, required=False)
child_assessment_update_parser.replace_argument('specialist_id', type=int, required=False)

# child_caregiver

child_caregiver_parser = reqparse.RequestParser()
child_caregiver_parser.add_argument('start_date', type=datetype, help=date_error_help)
child_caregiver_parser.add_argument('end_date', type=datetype, help=date_error_help)
child_caregiver_parser.add_argument('note')
child_caregiver_parser.add_argument('child_id', type=int, required=True)
child_caregiver_parser.add_argument('caregiver_id', type=int, required=True)

child_caregiver_update_parser = child_caregiver_parser.copy()
child_caregiver_update_parser.replace_argument('child_id', type=int, required=False)
child_caregiver_update_parser.replace_argument('caregiver_id', type=int, required=False)

# child_measurement

child_measurement_parser = reqparse.RequestParser()
child_measurement_parser.add_argument('date', required=True, type=datetype, help=date_error_help)
child_measurement_parser.add_argument('value', required=True, type=float)
child_measurement_parser.add_argument('child_id', type=int, required=True)
child_measurement_parser.add_argument('measurement_type_id', type=int, required=True)

child_measurement_update_parser = child_measurement_parser.copy()
child_measurement_update_parser.replace_argument('date', required=False, type=datetype, help=date_error_help)
child_measurement_update_parser.replace_argument('child_id', type=int, required=False)
child_measurement_update_parser.replace_argument('measurement_type_id', type=int, required=False)
child_measurement_update_parser.replace_argument('value', required=False, type=float)

# child_milestone

child_milestone_parser = reqparse.RequestParser()
child_milestone_parser.add_argument('date', required=True, type=datetype, help=date_error_help)
child_milestone_parser.add_argument('child_id', type=int, required=True)
child_milestone_parser.add_argument('milestone_type_id', type=int, required=True)

child_milestone_update_parser = child_milestone_parser.copy()
child_milestone_update_parser.replace_argument('date', required=False, type=datetype, help=date_error_help)
child_milestone_update_parser.replace_argument('child_id', type=int, required=False)
child_milestone_update_parser.replace_argument('milestone_type_id', type=int, required=False)

# child_doctor_visit

child_doctor_visit_parser = reqparse.RequestParser()
child_doctor_visit_parser.add_argument('date', required=True, type=datetype, help=date_error_help)
child_doctor_visit_parser.add_argument('child_id', type=int, required=True)
child_doctor_visit_parser.add_argument('doctor_id', type=int, required=True)
child_doctor_visit_parser.add_argument('note')

child_doctor_visit_update_parser = child_doctor_visit_parser.copy()
child_doctor_visit_update_parser.replace_argument('date', required=False, type=datetype, help=date_error_help)
child_doctor_visit_update_parser.replace_argument('child_id', type=int, required=False)
child_doctor_visit_update_parser.replace_argument('doctor_id', type=int, required=False)

# child_medical_condition

child_medical_condition_parser = reqparse.RequestParser()
child_medical_condition_parser.add_argument('child_id', type=int, required=True)
child_medical_condition_parser.add_argument('medical_condition_id', type=int, required=True)

child_medical_condition_update_parser = child_medical_condition_parser.copy()
child_medical_condition_update_parser.replace_argument('child_id', type=int, required=False)
child_medical_condition_update_parser.replace_argument('medical_condition_id', type=int, required=False)

# child_medication

child_medication_parser = reqparse.RequestParser()
child_medication_parser.add_argument('start_date', required=True, type=datetype, help=date_error_help)
child_medication_parser.add_argument('end_date', type=datetype, help=date_error_help)
child_medication_parser.add_argument('dosage1', type=float)
child_medication_parser.add_argument('dosage2', type=float)
child_medication_parser.add_argument('dosage3', type=float)
child_medication_parser.add_argument('child_id', type=int, required=True)
child_medication_parser.add_argument('medication_id', type=int, required=True)

child_medication_update_parser = child_medication_parser.copy()
child_medication_update_parser.replace_argument('start_date', required=False, type=datetype, help=date_error_help)
child_medication_update_parser.replace_argument('child_id', type=int, required=False)
child_medication_update_parser.replace_argument('medication_id', type=int, required=False)

################ Look Up Tables ###############

class EntityData:
    def __init__(self, class_type, marshaller, create_parser, update_parser):
        self.class_type = class_type
        self.marshaller = marshaller
        self.create_parser = create_parser
        self.update_parser = update_parser

entity_data = {
    'child'                  : EntityData(Child, child_fields, child_parser, child_update_parser),
    'child_note'             : EntityData(ChildNote, child_note_fields, child_note_parser, child_note_update_parser),
    'partner'                : EntityData(Partner, partner_fields, partner_parser, partner_update_parser),
    'caregiver'              : EntityData(Caregiver, caregiver_fields, caregiver_parser, caregiver_update_parser),
    'specialist'             : EntityData(Specialist, specialist_fields, specialist_parser, specialist_update_parser),
    'specialist_type'        : EntityData(SpecialistType, specialist_type_fields, specialist_type_parser, specialist_type_update_parser),
    'milestone_type_category': EntityData(MilestoneTypeCategory, milestone_type_category_fields, milestone_type_category_parser, milestone_type_category_update_parser),
    'milestone_type'         : EntityData(MilestoneType, milestone_type_fields, milestone_type_parser, milestone_type_update_parser),
    'doctor_type'            : EntityData(DoctorType, doctor_type_fields, doctor_type_parser, doctor_type_update_parser),
    'doctor'                 : EntityData(Doctor, doctor_fields, doctor_parser, doctor_update_parser),
    'measurement_type'       : EntityData(MeasurementType, measurement_type_fields, measurement_type_parser, measurement_type_update_parser),
    'camp'                   : EntityData(Camp, camp_fields, camp_parser, camp_update_parser),
    'medical_condition'      : EntityData(MedicalCondition, medical_condition_fields, medical_condition_parser, medical_condition_update_parser),
    'medication'             : EntityData(Medication, medication_fields, medication_parser, medication_update_parser),
    'child_partner'          : EntityData(ChildPartner, child_partner_fields, child_partner_parser, child_partner_update_parser),
    'child_camp'             : EntityData(ChildCamp, child_camp_fields, child_camp_parser, child_camp_update_parser),
    'child_assessment'       : EntityData(ChildAssessment, child_assessment_fields, child_assessment_parser, child_assessment_update_parser),
    'child_caregiver'        : EntityData(ChildCaregiver, child_caregiver_fields, child_caregiver_parser, child_caregiver_update_parser),
    'child_measurement'      : EntityData(ChildMeasurement, child_measurement_fields, child_measurement_parser, child_measurement_update_parser),
    'child_milestone'        : EntityData(ChildMilestone, child_milestone_fields, child_milestone_parser, child_milestone_update_parser),
    'child_doctor_visit'     : EntityData(ChildDoctorVisit, child_doctor_visit_fields, child_doctor_visit_parser, child_doctor_visit_update_parser),
    'child_medical_condition': EntityData(ChildMedicalCondition, child_medical_condition_fields, child_medical_condition_parser, child_medical_condition_update_parser),
    'child_medication'       : EntityData(ChildMedication, child_medication_fields, child_medication_parser, child_medication_update_parser)
}

entity_names = entity_data.keys()

################ Resources ####################

# Base resource class for resource data.
class ResourceBase(Resource):
    def __init__(self):
        self.ed = None
        self.query = None

    # Call this right away to populate the entity data object.
    def get_entity_data(self, name):
        if name not in entity_names:
            abort(404, message="Invalid entity name: '" + name + "'. Legal entity names are: " + ", ".join(entity_names))
        self.ed = entity_data[name]
        self.query = session.query(self.ed.class_type)
 
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

    def verify_filters(self):
        for attr in request.args.to_dict().keys():
            if not hasattr(self.ed.class_type, attr):
                abort (404, message= "Class {} does not have filter attribute {}!".format(self.ed.class_type.__name__, attr))


class EntityResource(ResourceBase):
    # GET to get instances by filter arguments (e.g. ?english_name=Bobby&sex=M).
    # No arguments returns all entities of that type.
    def get(self, entity_name):
        self.get_entity_data(entity_name)
        self.verify_filters()
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

class EntityFilterResource(ResourceBase):

    def post(self, entity_name):
        parser = self._make_filter_parser(entity_name)
        args = parser.parse_args()
        filters = []
        for arg in args.keys():
            for op_val_pair in args[arg]:
                try:
                    op, val = tuple(op_val_pair.split(','))
                except ValueError:
                    msg = "Improperly formatted query: {}. Use \"op,val\", e.g. \"eq,M\"".format(op_val_pair)
                    abort(400, message=msg)
                if op == 'eq':
                    filters.append(self._filter_eq(arg, val))
                elif op == 'lt':
                    filters.append(self._filter_lt(arg, val))
                elif op == 'gt':
                    filters.append(self._filter_gt(arg, val))
                else:
                    msg = "Attempted to filter {} by {} without specifying filter parameters".format(entity_name, args.attribute)
                    abort(400, message=msg)
        return {"filtered_entities": [marshal(res, self.ed.marshaller) for res in self.query.filter(and_(*filters)).all()]}

    def _filter_eq(self, attribute, val):
        return getattr(self.ed.class_type, attribute) == val

    def _filter_lt(self, attribute, val):
        return getattr(self.ed.class_type, attribute) < val

    def _filter_gt(self, attribute, val):
        return getattr(self.ed.class_type, attribute) > val

    def _make_filter_parser(self, entity_name):
        self.get_entity_data(entity_name)
        parser = reqparse.RequestParser()
        raw_json = request.get_json()
        for arg in self.ed.update_parser.args:
            if arg.name in raw_json.keys():
                parser.add_argument(arg.name, type=list, location='json')
        return parser


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
        session.rollback()
        response = { 'message': 'Successfully rolled back the session!' }
        return response, 200

# Resource for checking online status
class HeartbeatResource(ResourceBase):
    def get(self):
        response = { 'message': 'beat' }
        return response, 200
