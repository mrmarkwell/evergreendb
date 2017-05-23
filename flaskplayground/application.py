from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager


application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)
rest_api = Api(application)
login_manager = LoginManager(application)

from app.api.resources import QueryResource
from app.api.resources import EntityResource
from app.api.resources import EntityListResource
from app.api.resources import FilterResource
from app.api.resources import HeartbeatResource
from app.api.resources import RollbackResource
from app.api.upload import Upload
from app.api.resources import UserResource

rest_api.add_resource(QueryResource, "/query", endpoint="query")
rest_api.add_resource(EntityResource, "/entity/<string:entity_name>", endpoint="entity")
rest_api.add_resource(FilterResource, "/filter")
rest_api.add_resource(EntityListResource, "/entity", endpoint="entities")
rest_api.add_resource(HeartbeatResource, "/heartbeat", endpoint="heartbeat")
rest_api.add_resource(RollbackResource, "/rollback", endpoint="rollback")
rest_api.add_resource(Upload, "/upload")
rest_api.add_resource(UserResource, "/user")

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
