from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

import models

from resources import QueryResource
from resources import EntityResource
from resources import EntityListResource
from resources import HeartbeatResource
from resources import RollbackResource

api.add_resource(QueryResource, "/query", endpoint="query")
api.add_resource(EntityResource, "/entity/<string:entity_name>", endpoint="entity")
api.add_resource(EntityListResource, "/entity", endpoint="entities")
api.add_resource(HeartbeatResource, "/heartbeat", endpoint="heartbeat")
api.add_resource(RollbackResource, "/rollback", endpoint="rollback")


