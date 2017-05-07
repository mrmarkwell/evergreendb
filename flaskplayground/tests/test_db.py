import os
import unittest

from config import basedir
from app import app, db, models

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_child(self):
        child = models.Child(nickname=unicode('johnny'))
        db.session.add(child)
        db.session.commit()
        children = db.session.query(models.Child).all()
        self.assertEqual(len(children), 1)

if __name__ == '__main__':
    unittest.main()
