import forgery_py as fpy
from app.api.marshallers import Date
from app.api.entity_data import entity_data
from flask_restful import fields
from pprint import pprint as pp
import random

def get_test_data(num_records = 10):
    test_data = dict()
    for entity, ed in entity_data.items():
        test_data[entity] = list()
        for i in xrange(num_records):
            test_data[entity].append(dict())
            vals = test_data[entity][i]
            marshaller = ed.marshaller.copy()
            marshaller.pop('id', None)
            for field, field_type in marshaller.items():
                if field_type == fields.Integer:
                    vals[field] = fpy.basic.random.randint(1, num_records)
                if field_type == fields.Float:
                    vals[field] = float(random.randint(1000000, 9999999)) / 1000.0
                if field_type == fields.String:
                    if 'name'in field:
                        vals[field] = fpy.name.full_name()
                    elif 'email' in field:
                        vals[field] = fpy.internet.email_address()
                    elif 'sex' in field:
                        vals[field] = fpy.personal.gender()[0]
                    else:
                        vals[field] = fpy.lorem_ipsum.paragraph()
                if field_type == Date:
                    vals[field] = fpy.date.date().strftime('%Y-%m-%d')
                if field_type == fields.Boolean:
                    #vals[field] = fpy.basic.random.choice([1, 0])
                    vals[field] = 1
    
    return test_data
#pp(test_data)







