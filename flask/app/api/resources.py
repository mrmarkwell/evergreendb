from datetime import datetime
import json

from db import get_session
from marshallers import DATE_FMT

from sqlalchemy import text
from sqlalchemy.sql.expression import and_
from flask import request
from flask import jsonify

from marshallers import DATE_FMT

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import marshal
from entity_data import entity_data, entity_names

################ Resources ####################

# Base resource class for resource data.
class ResourceBase(Resource):
    def __init__(self):
        self.ed = None
        self.ed_list = list()
        self.query = None
        self.session = get_session()

    # Call this right away to populate the entity data object.
    def get_entity_data(self, name):
        if name not in entity_names:
            abort(404, message="Invalid entity name: '" + name + "'. Legal entity names are: " + ", ".join(entity_names))
        if self.ed is None:
            self.ed = entity_data[name]
        self.ed_list.append(entity_data[name])
        #self.query = self.session.query(self.ed.class_type)
 
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
        names = [x.strip() for x in entity_name.split(',')]
        for name in names:
            self.get_entity_data(name)
        marshaller = dict()
        classes = [x.class_type for x in self.ed_list]
        query = self.session.query()
        filters = request.args.to_dict()
        attrs = filters.keys()
        first = True
        for ed in self.ed_list:
            query = query.add_entity(ed.class_type)
            # Skip joining the first one. That's just how SQLAlchemy works.
            # We can't "join" the first table in the class list to itself.
            if not first:
                query = query.join(ed.class_type)
            marshaller.update(ed.marshaller)
            sub_attrs = [x for x in attrs if hasattr(ed.class_type, x)]
            sub_filters = [
                self.parse_filter(ed.class_type, attribute, filters[attribute]) for attribute in sub_attrs
            ]
            if sub_filters:
                query = query.filter(and_(*sub_filters))
            first = False
        # This is a hack to get the same query but without column labels
        # Not sure what the "right" way to do it is
        sq = query.subquery(with_labels=False)
        result = self.session.execute(sq)
        result_dict = []
        for row in result:
            result_dict.append(dict(zip(row.keys(), row)))
        return marshal(result_dict, marshaller), 200

    @classmethod
    def parse_filter(cls, e_class, attribute, filterblob):
        """parse filter with format "op,val", if op is left off
        it is assumed to be "eq"
        Available operations
            eq: equal
            ne: not equal
            gt: greater than
            ge: greater than or equal to
            lt: less than
            le: less than or equal to
            like: like
        """
        opval = filterblob.split(',')
        if len(opval) == 1:
            opval = ['eq'] + opval
        try:
            op, val = tuple(opval)
        except ValueError:
            msg = ("Improperly formatted filter {}. Use format 'op,val'"
                   " or just 'val' (default op is 'eq'). For example,"
                   " ?medication_id=gt,4".format(filterblob))
            abort(400, msg)
        try:
            val = datetime.strptime(val, DATE_FMT)
        except ValueError:
            pass
        if op == 'eq':
            return getattr(e_class, attribute) == val
        if op == 'lt':
            return getattr(e_class, attribute) < val
        if op == 'le':
            return getattr(e_class, attribute) <= val
        if op == 'gt':
            return getattr(e_class, attribute) > val
        if op == 'ge':
            return getattr(e_class, attribute) >= val
        if op == 'ne':
            return getattr(e_class, attribute) != val
        if op == 'like':
            return getattr(e_class, attribute).like(val)

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

    Available operations
        eq: equal
        ne: not equal
        gt: greater than
        ge: greater than or equal to
        lt: less than
        le: less than or equal to
        like: like
    """

    def post(self):
        """filter using eq, lt, gt, ne or like"""
        data = self._get_entity_data()
        results = []
        for e_class, e_marshaller, attributes, e_query in data:
            try:
                filters = self._build_filter(e_class, attributes)
            except (TypeError, AttributeError) as e:
                msg = ("Attempted to filter {}"
                       " without specifying filter parameters\n"
                       "Exception:\n{}".format(e_class, e))
                abort(400, message=msg)
            results.append({e_class.__tablename__: [marshal(res, e_marshaller) for res in e_query.filter(and_(*filters)).all()]})
        return {"filtered_entityes": results}

    def _build_filter(self, e_class, attributes):
        filters = []
        for attribute in attributes:
            for op, val in attributes[attribute].items():
                try:
                    val = datetime.strptime(val, DATE_FMT)
                except ValueError:
                    pass
                if op == 'eq':
                    filters.append(getattr(e_class, attribute) == val)
                elif op == 'lt':
                    filters.append(getattr(e_class, attribute) < val)
                elif op == 'le':
                    filters.append(getattr(e_class, attribute) <= val)
                elif op == 'gt':
                    filters.append(getattr(e_class, attribute) > val)
                elif op == 'ge':
                    filters.append(getattr(e_class, attribute) >= val)
                elif op == 'ne':
                    filters.append(getattr(e_class, attribute) != val)
                elif op == 'like':
                    filters.append(getattr(e_class, attribute).like(val))
                else:
                    raise AttributeError()
        return filters

    def _get_entity_data(self):
        data = []
        raw_json = request.get_json()
        for entity_name in raw_json.keys():
            self.get_entity_data(entity_name)
            data.append((self.ed.class_type, self.ed.marshaller, raw_json[entity_name], self.query))
        return data


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
class HeartbeatResource(ResourceBase):
    def get(self):
        response = {'message': 'beat'}
        return response, 200
