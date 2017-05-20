from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
rest_api = Api(app)

import models

from api.resources import QueryResource
from api.resources import EntityResource
from api.resources import EntityListResource
from api.resources import FilterResource
from api.resources import HeartbeatResource
from api.resources import RollbackResource
from api.upload import Upload

rest_api.add_resource(QueryResource, "/query", endpoint="query")
rest_api.add_resource(EntityResource, "/entity/<string:entity_name>", endpoint="entity")
rest_api.add_resource(FilterResource, "/filter")
rest_api.add_resource(EntityListResource, "/entity", endpoint="entities")
rest_api.add_resource(HeartbeatResource, "/heartbeat", endpoint="heartbeat")
rest_api.add_resource(RollbackResource, "/rollback", endpoint="rollback")
rest_api.add_resource(Upload, "/upload")