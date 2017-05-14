from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

import models

from api.resources import QueryResource
from api.resources import EntityResource
from api.resources import EntityListResource
from api.resources import EntityFilterResource
from api.resources import HeartbeatResource
from api.resources import RollbackResource
from api.upload import Upload

api.add_resource(QueryResource, "/query", endpoint="query")
api.add_resource(EntityResource, "/entity/<string:entity_name>", endpoint="entity")
api.add_resource(EntityFilterResource, "/entity/<string:entity_name>/filter")
api.add_resource(EntityListResource, "/entity", endpoint="entities")
api.add_resource(HeartbeatResource, "/heartbeat", endpoint="heartbeat")
api.add_resource(RollbackResource, "/rollback", endpoint="rollback")
api.add_resource(Upload, "/upload")
