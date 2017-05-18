from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from app import app

def get_session():
    Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(app.config["SQLALCHEMY_DATABASE_URI"]))
    session = scoped_session(Session)
    return session
