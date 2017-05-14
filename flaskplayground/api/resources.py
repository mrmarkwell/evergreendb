from datetime import datetime
import json

from db import session
from sqlalchemy import text
from sqlalchemy.sql.expression import and_
from flask import request
from flask import jsonify

from flask_restful import abort
from flask_restful import Resource
from flask_restful import marshal_with
from flask_restful import marshal
from entity_data import *
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
