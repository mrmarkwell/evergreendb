# -*- coding: utf-8 -*-
import json
import os
import unittest
import sys
import tempfile
import random

from pprint import pprint as pp
from hypothesis import given, settings
from hypothesis.strategies import composite, sampled_from
from rest_test_data import get_test_data


from app import app, db, models, login_manager
from config import basedir

reload(sys)
sys.setdefaultencoding('utf8')

BOBBY_DATA = {
  "abandonment_date": "2014-01-02",
  "birth_date": "2014-01-01",
  "child_history": "Bobby is from 充佛动囖",
  "child_chinese_name": "吃手婆娘给飘红",
  "child_english_name": "Bobby",
  "medical_history": "Bobby had a fever",
  "nickname": "Little Bobby Tables",
  "child_pinyin_name": "ch po en",
  "program_departure_date": None,
  "program_departure_reason": None,
  "program_entry_date": "2014-01-03",
  "sex": "M"
}

class TestFlaskRestApi(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
           os.path.join(basedir, 'test.db')
        db.create_all()
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        login_manager._login_disabled = True
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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

class TestEntityEndpoint(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
           os.path.join(basedir, 'test.db')
        db.create_all()
        app.config['LOGIN_DISABLED'] = True
        login_manager._login_disabled = True
        self.app = app.test_client()
        self.debug = False # set this to true for more logging
        self.seed = None # set the random seed here if we want to reproduce a bug found by TravisCI

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post(self):
        if self.seed is None:
            self.seed = random.randint(1, 10000)
        print "RANDOM SEED USED: " + str(self.seed)
        random.seed(self.seed)
        test_data = get_test_data()
        for i in xrange(30): 
            
            e_name = random.choice(test_data.keys())
            #skipping user because its actually not valid currently...
            if (e_name == "user"):
                break
            e_body = random.choice(test_data[e_name])
            if self.debug: pp(e_name)
            if self.debug: pp(e_body)
            if self.debug: print
            post_response = self.app.post('/entity/' + e_name, data=e_body)
            if self.debug: pp(post_response.get_data())
            res_body = json.loads(post_response.get_data())
            if self.debug: pp(res_body)
            id = res_body.pop('id', None)
            delete_response = self.app.delete('/entity/' + e_name + "?id=" + str(id))
            if self.debug: print delete_response.status_code

            self.assertEqual(post_response.status_code, 201, "Post failed")
            self.assertDictEqual(res_body, e_body, "Post sent back bad data")
            self.assertEqual(delete_response.status_code, 204, "Delete failed")
        
#    def test_fake(self):
#        data = {'child_id': 60,
#                'date': '2017-05-22',
#                'flag': 1,
#                'note': '3VFdZ7FitwX89ksodZkJDxgKaCRJoQIfj4xy3ZSiUIuqmqjFRQfaLxGh9RxxcxdePwZ1wUfW7yGcAxPv'}
#        #json_data = json.dumps(data)
#        #str_data = str(data)
#       # pp(json_data)
#       # pp(str_data)
#        print "hello"
#         
#        for i in xrange(30): 
#            post_response = self.app.post('/entity/child_note', data=data)
#            pp(post_response.get_data())
#

if __name__ == "__main__":
    unittest.main()
