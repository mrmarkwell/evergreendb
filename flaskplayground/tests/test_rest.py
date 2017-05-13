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

if __name__ == "__main__":
    unittest.main()