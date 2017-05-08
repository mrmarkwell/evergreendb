from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

import models

from resources import ChildResource, ChildListResource
from resources import QueryResource

api.add_resource(ChildListResource, "/children", endpoint="children")
api.add_resource(ChildResource, "/child/<string:id>", endpoint="child")
api.add_resource(QueryResource, "/query", endpoint="query")
