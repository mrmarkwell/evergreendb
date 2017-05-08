from app.models import Child
from db import session
from datetime import datetime
from werkzeug.datastructures import FileStorage
from sqlalchemy import text

from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

datetype = lambda x: datetime.strptime(x, '%Y-%m-%d')
date_error_help = "Date fields should be entered as: YYYY-MM-DD"
row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

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
    'uri': fields.Url('child', absolute=True)
}

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

class ChildResource(Resource):
    @marshal_with(child_fields)
    def get(self, id):
        child = session.query(Child).filter(Child.id == id).first()
        if not child:
            abort(404, message="Child {} doesn't exist".format(id))
        return child, 200

    def delete(self, id):
        child = session.query(Child).filter(Child.id == id).first()
        if not child:
            abort(404, message="Child {} doesn't exist".format(id))
        session.delete(child)
        session.commit()
        return {}, 204

    @marshal_with(child_fields)
    def put(self, id):
        args = child_parser.parse_args()
        child = session.query(Child).filter(Child.id == id).first()
        child.english_name = args['english_name']
        session.add(child)
        session.commit()
        return child, 201
    
    
class ChildListResource(Resource):
    @marshal_with(child_fields)
    def get(self):
        children = session.query(Child).all()
        return children, 200

    @marshal_with(child_fields)
    def post(self):
        args = child_parser.parse_args()
        child = Child(english_name=args['english_name'])
        session.add(child)
        session.commit()
        return child, 201


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
        
