"""Migration script to be run whenever there changes in app database structure"""

from __future__ import print_function
import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

VERSION = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
MIGRATION = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (VERSION + 1))
TMP_MODULE = imp.new_module('old_model')
OLD_MODEL = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

exec(OLD_MODEL, TMP_MODULE.__dict__)

SCRIPT = api.make_update_script_for_model(
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_MIGRATE_REPO,
    TMP_MODULE.meta,
    db.metadata
)
open(MIGRATION, "wt").write(SCRIPT)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
VERSION = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + MIGRATION)
print('Current database version: ' + str(VERSION))
