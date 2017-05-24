import json

from flask import g
from db import get_session
from sqlalchemy import text
from sqlalchemy.sql.expression import and_
from flask import request, current_app
from flask import jsonify
from pprint import pprint as pp

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import marshal
from entity_data import entity_data, entity_names

from app import login_manager
from app.models import User
from functools import wraps
from flask_login import current_user, login_required


def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_app.config.get("LOGIN_DISABLED"): return f(*args, **kwargs)
        if current_user.is_authenticated and current_user.is_admin:
            # invoke the wrapped function
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrapped


def editor_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_app.config.get("LOGIN_DISABLED"): return f(*args, **kwargs)
        if current_user.is_authenticated and current_user.is_editor:
            # invoke the wrapped function
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrapped


@login_manager.request_loader
def load_user_from_request(request):
    if request.authorization:
        username, password = request.authorization.username, request.authorization.password

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return user
    return None

################ Resources ####################

# Base resource class for resource data.
class ResourceBase(Resource):
    decorators = [login_required]
    def __init__(self):
        self.ed = None
        self.query = None
        self.session = get_session()

    # Call this right away to populate the entity data object.
    def get_entity_data(self, name):
        if name not in entity_names:
            abort(404, message="Invalid entity name: '" + name + "'. Legal entity names are: " + ", ".join(entity_names))
        self.ed = entity_data[name]
        self.query = self.session.query(self.ed.class_type)
 
    # For operations that can only be performed on one entity, get that entity by id
    # Throw an error if 'id' was not specified in the request.
    def get_entity_by_id(self):
        id = request.args.to_dict().get("id", None)
        if not id:
            abort(404, message="This operation must be passed a specific entity ID!")
        entity = self.query.filter(self.ed.class_type.id == id).first()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(self.ed.class_type.__tablename__, id))
        return entity

    def verify_filters(self):
        for attr in request.args.to_dict().keys():
            if not hasattr(self.ed.class_type, attr):
                abort (404, message="Class {} does not have filter attribute {}!".format(self.ed.class_type.__name__, attr))


class EntityResource(ResourceBase):
    # GET to get instances by filter arguments (e.g. ?english_name=Bobby&sex=M).
    # No arguments returns all entities of that type.
    def get(self, entity_name):
        self.get_entity_data(entity_name)
        self.verify_filters()
        entity = self.query.filter_by(**request.args.to_dict()).all()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(entity_name, request.args.to_dict()))
        return marshal(entity, self.ed.marshaller), 200

    # DELETE to delete a single entity instance
    def delete(self, entity_name):
        self.get_entity_data(entity_name)
        entity = self.get_entity_by_id()
        self.session.delete(entity)
        self.session.commit()
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
        self.session.add(entity)
        self.session.commit()
        return marshal(entity, self.ed.marshaller), 201

    # Post to create a new entity
    def post(self, entity_name):
        self.get_entity_data(entity_name)
        entity_args = self.ed.create_parser.parse_args()
        entity = self.ed.class_type()
        for key in entity_args.keys():
            setattr(entity, key, entity_args[key])
        self.session.add(entity)
        self.session.commit()
        return marshal(entity, self.ed.marshaller), 201


# Resource for getting valid entity names.
class EntityListResource(ResourceBase):
    def get(self):
        response = {"entity_names": entity_names}
        return response, 200

class FilterResource(ResourceBase):
    """Filter with format like,
        {
        "child": {
            "sex": {
                "eq": "M"
            }
            "english_name": {
                "eq": "Bobby"
            }
          }
        }
    """

    # decorators = [editor_required]

    def post(self):
        """filter using eq, lt, gt, ne or like"""
        filters = []
        entity_data = self._get_entity_data()
        for e_class, e_marshaller, e_parser in entity_data:
#            attributes = e_parser.parse_args()
            attributes = e_parser
            for attribute in attributes:
                try:
                    for op, val in attributes[attribute].items():
                        if op == 'eq':
                            filters.append(self._filter_eq(e_class, attribute, val))
                        elif op == 'lt':
                            filters.append(self._filter_lt(e_class, attribute, val))
                        elif op == 'gt':
                            filters.append(self._filter_gt(e_class, attribute, val))
                        elif op == 'ne':
                            filters.append(self._filter_ne(e_class, attribute, val))
                        elif op == 'like':
                            filters.append(self._filter_like(e_class, attribute, val))
                        else:
                            raise AttributeError()
                except (TypeError, AttributeError) as e:
                    msg = "Attempted to filter {} without specifying filter parameters\nException:\n{}".format(e_class, e)
                    abort(400, message=msg)
        return {"filtered_entities": [marshal(res, self.ed.marshaller) for res in self.query.filter(and_(*filters)).all()]}

    def _filter_eq(self, e_class, attribute, val):
        return getattr(e_class, attribute) == val

    def _filter_lt(self, e_class, attribute, val):
        return getattr(e_class, attribute) < val

    def _filter_gt(self, e_class, attribute, val):
        return getattr(e_class, attribute) > val

    def _filter_ne(self, e_class, attribute, val):
        return getattr(e_class, attribute) != val

    def _filter_like(self, e_class, attribute, val):
        return getattr(e_class, attribute).like(val)

    def _get_entity_data(self):
        entity_data = []
        raw_json = request.get_json()
        for entity_name in raw_json.keys():
            parser = reqparse.RequestParser()
            self.get_entity_data(entity_name)
#            for arg in self.ed.update_parser.args:
#                if arg.name in raw_json[entity_name]:
#                    parser.add_argument(arg.name, type=dict, location='json')
#            entity_data.append((self.ed.class_type, self.ed.marshaller, parser))
            entity_data.append((self.ed.class_type, self.ed.marshaller, raw_json[entity_name]))
        return entity_data


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
        result = self.session.execute(sql)
        result_dict = []
        for row in result:
            result_dict.append(dict(zip(row.keys(), row)))
        return result_dict, 200
 
# Resource for calling a session.rollback()
class RollbackResource(ResourceBase):
    def post(self):
        self.session.rollback()
        response = {'message': 'Successfully rolled back the session!'}
        return response, 200

# Resource for checking online status
class HeartbeatResource(Resource):
    def get(self):
        response = {'message': 'beat'}
        return response, 200


class UserResource(ResourceBase):
    decorators = [admin_required]
    def get(self):
        self.get_entity_data("user")
        self.verify_filters()
        entity = self.query.filter_by(**request.args.to_dict()).all()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format("user", request.args.to_dict()))
        return marshal(entity, self.ed.marshaller), 200

    # DELETE to delete a single entity instance
    def delete(self):
        self.get_entity_data("user")
        entity = self.get_entity_by_id()
        self.session.delete(entity)
        self.session.commit()
        return {}, 204

    # PUT to update a single entity instance
    def put(self):
        self.get_entity_data("user")
        entity = self.get_entity_by_id()
        entity_args = self.ed.update_parser.parse_args()
        raw_json = request.get_json()
        for key in entity_args.keys():
            # Only update keys that are sent in the Json body
            if key in raw_json.keys():
                setattr(entity, key, entity_args[key])
        if "password" in raw_json.keys() :
            entity.hash_password(entity.password)
        self.session.add(entity)
        self.session.commit()
        return marshal(entity, self.ed.marshaller), 201

    # Post to create a new entity
    def post(self):
        self.get_entity_data("user")
        entity_args = self.ed.create_parser.parse_args()
        entity = self.ed.class_type()
        for key in entity_args.keys():
            setattr(entity, key, entity_args[key])
        entity.hash_password(entity.password)
        self.session.add(entity)
        self.session.commit()
        return marshal(entity, self.ed.marshaller), 201