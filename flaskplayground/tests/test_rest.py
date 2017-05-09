import unittest
import json
from app import app

class TestFlaskRestApi(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_heartbeat(self):
        response = self.app.get('/heartbeat')
        self.assertEqual(json.loads(response.get_data()), {'message': 'beat'})

if __name__ == "__main__":
    unittest.main()