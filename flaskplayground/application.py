from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager, UserMixin, login_required
from flask import request

application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)
api = Api(application)
login_manager = LoginManager()
login_manager.init_app(application)

import app.models as models
import base64

from resources import QueryResource
from resources import EntityResource
from resources import EntityListResource
from resources import HeartbeatResource
from resources import RollbackResource

api.add_resource(QueryResource, "/query", endpoint="query")
api.add_resource(EntityResource, "/entity/<string:id>", endpoint="entity")
api.add_resource(EntityListResource, "/entity", endpoint="entities")
api.add_resource(HeartbeatResource, "/heartbeat", endpoint="heartbeat")
api.add_resource(RollbackResource, "/rollback", endpoint="rollback")

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

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()