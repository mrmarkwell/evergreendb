import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'soar.db')
SQLALCHEMY_BINDS = { 
    'soar': SQLALCHEMY_DATABASE_URI,
    'fss': 'sqlite:///' + os.path.join(basedir, 'fss.db') }
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

LOGIN_DISABLED = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_TRACK_MODIFICATIONS = False
