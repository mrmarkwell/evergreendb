from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin, login_required
from flask import request


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
rest_api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

import models
import base64

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

class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('Authorization')

    if token is not None:
        token = token.replace('Basic ', '', 1)
        try:
            token = base64.b64decode(token)
        except TypeError:
            pass
        username, password = token.split(":")
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None
