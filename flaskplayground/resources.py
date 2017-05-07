from app.models import Child
from db import session
from datetime import datetime
from werkzeug.datastructures import FileStorage

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

child_fields = {
    'id': fields.Integer,
    'english_name': fields.String,
    'chinese_name': fields.String,
    'pinyin_name': fields.String,
    'nickname': fields.String,
    'sex': fields.String,
    'birth_date': fields.DateTime,
    'abandonment_date': fields.DateTime,
    'program_entry_date': fields.DateTime,
    'program_departure_date': fields.DateTime,
    'program_departure_reason': fields.String,
    'child_history': fields.String,
    'medical_history': fields.String,
    'is_active': fields.Boolean,
    'uri': fields.Url('child', absolute=True)
}

child_parser = reqparse.RequestParser()
child_parser.add_argument('english_name', required=True)
child_parser.add_argument('chinese_name')
child_parser.add_argument('pinyin_name')
child_parser.add_argument('nickname')
child_parser.add_argument('sex')
child_parser.add_argument('birth_date', type=datetime) 
child_parser.add_argument('abandonment_date', type=datetime)
child_parser.add_argument('program_entry_date', type=datetime)
child_parser.add_argument('program_departure_date', type=datetime)
child_parser.add_argument('program_departure_reason')
child_parser.add_argument('child_history')
child_parser.add_argument('medical_history')
child_parser.add_argument('is_active', type=bool)

class ChildResource(Resource):
    @marshal_with(child_fields)
    def get(self, id):
        child = session.query(Child).filter(Child.id == id).first()
        if not child:
            abort(404, message="Child {} doesn't exist".format(id))
        return child

    def delete(self, id):
        child = session.query(Child).filter(Child.id == id).first()
        if not child:
            abort(404, message="Child {} doesn't exist".format(id))
        session.delete(child)
        session.commit()
        return {}, 204

    @marshal_with(child_fields)
    def put(self, id):
        parsed_args = child_parser.parse_args()
        child = session.query(Child).filter(Child.id == id).first()
        child.english_name = parsed_args['english_name']
        session.add(child)
        session.commit()
        return child, 201
    
    @marshal_with(child_fields)
    def post(self):
        parsed_args = child_parser.parse_args()
        child = Child(english_name=parsed_args['english_name'])
        session.add(child)
        session.commit()
        return child, 201


class ChildListResource(Resource):
    @marshal_with(child_fields)
    def get(self):
        children = session.query(Child).all()
        return children

    @marshal_with(child_fields)
    def post(self):
        parsed_args = child_parser.parse_args()
        child = Child(english_name=parsed_args['english_name'])
        session.add(child)
        session.commit()
        return child, 201
