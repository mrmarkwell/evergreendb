"""Database creation script. Also handles creation of migration repository
if needed
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app.models import User
import os.path
from app import db
from app.api.db import get_session

def add_admin():
    # adding a default admin user to db create so that there is a user populated for use by frontend
    admin_user = User()
    admin_user.username = unicode("admin")
    admin_user.hash_password(unicode("admin"))
    admin_user.is_admin = True
    admin_user.is_editor = True
    session = get_session()
    session.add(admin_user)
    session.commit()



db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    add_admin()
    api.version_control(
        SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_MIGRATE_REPO,
        api.version(SQLALCHEMY_MIGRATE_REPO)
    )
