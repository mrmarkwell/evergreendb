import json
import os
import unittest

from app import app, db, models
from config import basedir

class TestFlaskRestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()
        bobby = models.Child(
            english_name="Robert",
            program_entry_date="2003-01-01",
            program_departure_date="2005-12-31",
            program_departure_reason="adoption",
            nickname="Bobby"
        )
        db.session.add_all([bobby])

    def setUp(self):
        self.app = app.test_client()

    def test_heartbeat(self):
        response = self.app.get('/heartbeat')
        self.assertEqual(json.loads(response.get_data()), {'message': 'beat'})

    def test_filter(self):
#        body = "{'id': {'gt': 0, 'lt': 5}, 'program_entry_date': {'gt': '1999-01-01'}, 'english_name': {'eq': 'Robert'}}"
#        body = {'id': ['gt:0', 'lt:5'], 'program_entry_date': ['gt:1999-01-01'], 'english_name': ['eq:Robert']}
#        body = {'id': 'gt:0,lt:5', 'program_entry_date': 'gt:1999-01-01', 'english_name': 'eq:Robert'}
        body = "id:gt=0,lt=5&program_entry_date:gt=199-01-01&english_name=Robert"
        response = self.app.get('/entity/child/filter', data=body)
        self.assertNotEqual(json.loads(response.get_data()), {})

if __name__ == "__main__":
    unittest.main()