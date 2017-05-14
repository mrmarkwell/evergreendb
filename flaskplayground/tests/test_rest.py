# -*- coding: utf-8 -*-
import json
import os
import unittest
import sys

from hypothesis import given
from hypothesis.strategies import composite, sampled_from
from rest_test_data import test_data

from app import app, db, models
from config import basedir

reload(sys)
sys.setdefaultencoding('utf8')

BOBBY_DATA = {
  "abandonment_date": "2014-01-02",
  "birth_date": "2014-01-01",
  "child_history": "Bobby is from 充佛动囖",
  "chinese_name": "吃手婆娘给飘红",
  "english_name": "Bobby",
  "medical_history": "Bobby had a fever",
  "nickname": "Little Bobby Tables",
  "pinyin_name": "ch po en",
  "program_departure_date": None,
  "program_departure_reason": None,
  "program_entry_date": "2014-01-03",
  "sex": "M"
}

sample_child_note = {
  "child_id": 1,
  "date": "2012-11-14",
  "flag": True,
  "id": 1,
  "note": "This is a note about a child!"
}

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
        res_dict = json.loads(response.get_data())
        # Remove the id field from the response
        res_dict.pop('id', None)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(res_dict, BOBBY_DATA)

from pprint import pprint as pp
@composite
def entity_data(draw):
    entity = draw(sampled_from(test_data.keys()))
    body = draw(sampled_from(test_data[entity]))
    return (entity, body)


class TestEntityEndpoint(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestEntityEndpoint, self).__init__(*args, **kwargs)
        self.app = app.test_client()

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()

    @given(entity_data())
    def test_post(self, ed):
        e_name, e_body = ed
        response = self.app.post('/entity/' + e_name, data=e_body)
        res_body = json.loads(response.get_data())
        res_body.pop('id', None)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(res_body, e_body)
    
    
if __name__ == "__main__":
    unittest.main()