# -*- coding: utf-8 -*-
import json
import os
import unittest

from app import app, db, models
from config import basedir

BOBBY_DATA = "{\n  \"abandonment_date\": \"2014-1-2\",\n  \"birth_date\": \"2014-1-1\",\n  \"child_history\": \"Bobby is from 充佛动囖\",\n  \"chinese_name\": \"吃手婆娘给飘红\",\n  \"english_name\": \"Bobby\",\n  \"medical_history\": \"Bobby had a fever\",\n  \"nickname\": \"Little Bobby Tables\",\n  \"pinyin_name\": \"ch po en\",\n  \"program_departure_date\": null,\n  \"program_departure_reason\": null,\n  \"program_entry_date\": \"2014-1-3\",\n  \"sex\": \"M\"\n}"

class TestFlaskRestApi(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFlaskRestApi, self).__init__(*args, **kwargs)
        self.app = app.test_client()

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

    def test_heartbeat(self):
        response = self.app.get('/heartbeat')
        self.assertEqual(json.loads(response.get_data()), {'message': 'beat'})

    def test_create_child(self):
        response = self.app.post('/entity/child', data=BOBBY_DATA)
        self.assertEqual(json.loads(response.get_data()), BOBBY_DATA)
        
if __name__ == "__main__":
    unittest.main()