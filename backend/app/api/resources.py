from datetime import datetime
import json
import csv
from csvcols import column_names_and_order
from config import basedir

from flask import g
from marshallers import DATE_FMT

from sqlalchemy import text
from sqlalchemy.sql.expression import and_
from flask import request, current_app
from flask import jsonify

from marshallers import DATE_FMT

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import marshal
from entity_data import entity_data, entity_names

from app import login_manager, db
from app.models import User
from functools import wraps
from flask_login import current_user, login_required
import os

from mailmerge import MailMerge

from pprint import pprint as pp

current_version = 0.1

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_app.config.get("LOGIN_DISABLED"):
            return f(*args, **kwargs)
        if current_user.is_authenticated and current_user.is_admin:
            # invoke the wrapped function
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrapped


def editor_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_app.config.get("LOGIN_DISABLED"):
            return f(*args, **kwargs)
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
        self.ed_list = list()
        self.query = None
        self.session = db.session

    # Call this right away to populate the entity data object.
    def get_entity_data(self, name):
        if name not in entity_names:
            abort(404, message="Invalid entity name: '" + name +
                  "'. Legal entity names are: " + ", ".join(entity_names))
        if self.ed is None:
            self.ed = entity_data[name]
        self.ed_list.append(entity_data[name])
        self.query = self.session.query(self.ed.class_type)

    # For operations that can only be performed on one entity, get that entity by id
    # Throw an error if 'id' was not specified in the request.
    def get_entity_by_id(self):
        id = request.args.to_dict().get("id", None)
        if not id:
            abort(404, message="This operation must be passed a specific entity ID!")
        entity = self.query.filter(self.ed.class_type.id == id).first()
        if not entity:
            abort(404, message="Entity {}: {} doesn't exist".format(
                self.ed.class_type.__tablename__, id))
        return entity

    def verify_filters(self):
        for attr in request.args.to_dict().keys():
            if not hasattr(self.ed.class_type, attr):
                abort(404, message="Class {} does not have filter attribute {}!".format(
                    self.ed.class_type.__name__, attr))


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

    # decorators = [editor_required]

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
            results.append({e_class.__tablename__: [marshal(
                res, e_marshaller) for res in e_query.filter(and_(*filters)).all()]})
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
            data.append((self.ed.class_type, self.ed.marshaller,
                         raw_json[entity_name], self.query))
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
        print sql
        result = self.session.execute(sql)
        result_dict = []
        for row in result:
            result_dict.append(dict(zip(row.keys(), row)))
        return result_dict, 200


class ReportResource(ResourceBase):
    def get(self, format_name):
        if (format_name in ("child.csv", "family.csv", "pathway.csv", "interaction.csv", "fss.csv")):
            result = self.generate_csv_report(format_name)
        elif (format_name.endswith(".docx")):
            result = self.generate_docx_report(format_name)
        else:
            abort(404, message="Format " + format_name +
                  " is not a valid report format")
        return result, 200

    def generate_docx_report(self, report):
        splitted = report.split('.')
        child_id = int(splitted[0])
        report_type = '.'.join(splitted[1:])
        template = os.path.join(basedir,'docx-templates',report_type)
        root_dir = os.path.join(basedir, 'app')
        report_file_name = os.path.join('static',report) # should be with child name not id
        report_file_path = os.path.join(root_dir,report_file_name)
        doc = MailMerge(template)
        doc.merge(**self.get_docx_template_fields(child_id))
        doc.write(report_file_path)
        return report_file_name

    def get_docx_template_fields(self,child_id):
        fss_child = entity_data["fss_child"].class_type
        result = self.session.query(fss_child).get(child_id)
        return result.__dict__

    def generate_csv_report(self, report):
        fss_child = entity_data["fss_child"].class_type
        fss_family_member = entity_data["fss_family_member"].class_type
        fss_interaction = entity_data["fss_interaction"].class_type
        fss_projected_pathway = entity_data["fss_projected_pathway"].class_type
        #query = self.session.query(fss_child, fss_family_member, fss_interaction, fss_projected_pathway) \
        #    .join(fss_family_member).join(fss_interaction).join(fss_projected_pathway)
        if (report == "child.csv"):
            query = self.session.query(fss_child)
        elif (report == "family.csv"):
            query = self.session.query(fss_child, fss_family_member).join(fss_family_member)
        elif (report == "pathway.csv"):
            query = self.session.query(fss_child, fss_projected_pathway).join(fss_projected_pathway)
        elif (report == "interaction.csv"):
            query = self.session.query(fss_child, fss_interaction).join(fss_interaction)
        elif (report == "fss.csv"):
            query = self.session.query(fss_child, fss_family_member, fss_interaction, fss_projected_pathway) \
                .outerjoin(fss_family_member).outerjoin(fss_interaction).outerjoin(fss_projected_pathway)
        result = self.session.execute(query)

        return self.write_csv_report(report, result)

    def write_csv_report(self, report, result):
        # Convert to a true list of dicts
        columns = column_names_and_order[report]
        converted_result = []
        for r in result:
            converted_result.append(dict())
            for k,v in r.items():
                try:
                    converted_result[-1][columns[k]] = v
                except: pass
        result = converted_result
        keys = columns.values()
        # write out to file
        dest_dir = os.path.join(basedir, 'app')
        report_file_name = os.path.join('static',report)
        with open(os.path.join(dest_dir,report_file_name), 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(result)

        return report_file_name


class EnumResource(Resource):
    def put(self, enum_name):
        vals = set(request.get_json())
        EnumResource.set_list_by_name(enum_name, vals)
        return list(vals), 201

    def get(self, enum_name):
        result = EnumResource.get_list_by_name(enum_name)
        if not result:
            abort(404, message="No enum exists with name " + enum_name + "!")
        return result, 200

    @classmethod
    def set_list_by_name(cls, name, vals):
        filepath = os.path.join("enums", name + ".csv")

        with open(filepath, "a+") as f:
            f.write(",".join(vals) + "\n")

    @classmethod
    def get_list_by_name(cls, name):
        filepath = os.path.join("enums", name + ".csv")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                return None
            result = lines[-1].strip().split(",")
            return result

class ReminderResource(ResourceBase):
    def get(self):
        response = self.gen_reminder_list()
        return response, 200

    def gen_reminder_list(self):
        fss_child = entity_data["fss_child"].class_type
        fss_interaction = entity_data["fss_interaction"].class_type
        fss_projected_pathway = entity_data["fss_projected_pathway"].class_type

        query = self.session.query(fss_child, fss_interaction).join(fss_interaction)
        interactions = self.session.execute(query)
        reminders = self.reminders_from_interactions(interactions)
        query = self.session.query(fss_child, fss_projected_pathway).join(fss_projected_pathway)
        projected_pathways = self.session.execute(query)
        reminders.extend(self.reminders_from_projected_pathways(projected_pathways))

        reminders.sort(key=lambda rem: rem["date"])
        reminders = [ r for r in reminders if r["date"] >= datetime.today().strftime(DATE_FMT)]
        return reminders

    def reminders_from_interactions(self, interactions):
        reminders = []
        for interaction in interactions:
            reminders.append({
                "child_id":interaction["fss_child_id"],
                "child_pinyin_name":interaction["fss_child_child_pinyin_name"],
                "child_chinese_name":interaction["fss_child_child_chinese_name"],
                "child_nickname":interaction["fss_child_nickname"],
                "date":interaction["fss_interaction_interaction_date"].strftime(DATE_FMT),
                "type":interaction["fss_interaction_interaction_type"],
                "notes":interaction["fss_interaction_interaction_notes"]
            })
        return reminders

    def reminders_from_projected_pathways(self, projected_pathways):
        reminders = []
        for projected_pathway in projected_pathways:
            reminders.append({
                "child_id":projected_pathway["fss_child_id"],
                "child_pinyin_name":projected_pathway["fss_child_child_pinyin_name"],
                "child_chinese_name":projected_pathway["fss_child_child_chinese_name"],
                "child_nickname":projected_pathway["fss_child_nickname"],
                "date":projected_pathway["fss_projected_pathway_pathway_completion_date"].strftime(DATE_FMT),
                "type":"Projected Pathway",
                "notes":projected_pathway["fss_projected_pathway_pathway_short_description"]
            })
        return reminders

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

# Resource for checking version
class VersionResource(Resource):
    def get(self):
        response = current_version
        return response, 200

class AuthCheckResource(Resource):

    @login_required
    def get(self):
        response = {'message': 'success'}
        return response, 200


class AdminAuthCheckResource(Resource):

    @admin_required
    def get(self):
        response = {'message': 'success'}
        return response, 200


class UserResource(ResourceBase):
    decorators = []

    @login_required
    def get(self):
        self.get_entity_data("user")
        self.verify_filters()
        if current_user.is_admin:
            entity = self.query.filter_by(**request.args.to_dict()).all()
            if not entity:
                abort(404, message="Entity {}: {} doesn't exist".format(
                    "user", request.args.to_dict()))
            return marshal(entity, self.ed.marshaller), 200
        else:
            if request.args.to_dict():
                abort(
                    403, message="Permission denied, pass with no args to get your user data")
            else:
                return marshal([current_user], self.ed.marshaller), 200

    # DELETE to delete a single entity instance
    @admin_required
    def delete(self):
        self.get_entity_data("user")
        entity = self.get_entity_by_id()
        self.session.delete(entity)
        self.session.commit()
        return {}, 204

    # PUT to update a single entity instance
    @login_required
    def put(self):
        self.get_entity_data("user")
        entity = self.get_entity_by_id()
        # prevent users that are not admins from changing other users settings
        if entity.id != current_user.id and not current_user.is_admin:
            abort(403, message="Permission denied, only admins can modify another user")
        entity_args = self.ed.update_parser.parse_args()
        raw_json = request.get_json()
        # only allow admins to change other properties besides password
        admin_only = ["is_admin", "is_editor", "username"]
        for key in entity_args.keys():
            # Only update keys that are sent in the Json body
            if key in raw_json.keys():
                if key not in admin_only or current_user.is_admin:
                    setattr(entity, key, entity_args[key])
        if "password" in raw_json.keys():
            entity.hash_password(entity.password)
        self.session.add(entity)
        self.session.commit()
        return marshal(entity, self.ed.marshaller), 201

    # Post to create a new entity
    @admin_required
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
