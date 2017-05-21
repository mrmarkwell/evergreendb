from tests.rest_test_data import get_test_data
from app.api.db import get_session
from app import app
import sys

num_records = 10
if len(sys.argv) > 1:
    num_records = int(sys.argv[1])


session = get_session()
test_data = get_test_data(num_records)
client = app.test_client()
for entity in test_data.keys():
    for data in test_data[entity]:
        print "adding " + entity
        response = client.post('/entity/' + entity, data=data)
        if response.status_code != 201:
            print "Something bad happened during DB seed! Exiting!"
            exit(1)
