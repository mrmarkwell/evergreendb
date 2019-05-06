import forgery_py as fpy
from app.api.marshallers import Date
from production_seed_data import *
from app.api.entity_data import entity_data
from flask_restful import fields
from pprint import pprint as pp
import random


def get_test_data(num_records=10):
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
                    maxval = num_records
                    if field == "specialist_type_id":
                        maxval = 4
                    if field == "milestone_type_id":
                        maxval = 21
                    if field == "milestone_type_category_id":
                        maxval = 3
                    if field == "doctor_type_id":
                        maxval = 7
                    if field == "measurement_type_id":
                        maxval = 4
                    if field == "camp_id":
                        maxval = 3
                    if field == "medication_id":
                        maxval = 8
                    if field == "medical_condition_id":
                        maxval = 17
                    vals[field] = fpy.basic.random.randint(1, maxval)
                if field_type == fields.Float:
                    vals[field] = float(random.randint(
                        1000000, 9999999)) / 1000.0
                if field_type == fields.String:
                    if 'name' in field:
                        vals[field] = fpy.name.full_name()
                    elif 'phone' in field or 'wechat' in field:
                        vals[field] = fpy.address.phone()
                    elif 'interaction_coordinator' in field:
                        vals[field] = random.choice(interaction_coordinators)
                    elif 'interaction_type' in field:
                        vals[field] = random.choice(interaction_types)
                    elif field.endswith('diagnosis'):
                        vals[field] = random.choice(medical_conditions)
                    elif 'relationship' in field or 'people_present' in field:
                        vals[field] = random.choice(["Mother", "Father", "Grandmother", "Grandfather", "Other"])
                    elif 'email' in field:
                        vals[field] = fpy.internet.email_address()
                    elif 'sex' in field or 'gender' in field:
                        vals[field] = fpy.personal.gender()[0]
                    elif 'address' in field:
                        vals[field] = '%s, %s, %s %s'%(fpy.address.street_address(), 
                            fpy.address.city(), fpy.address.country(), fpy.address.zip_code())
                    else:
                        vals[field] = fpy.lorem_ipsum.paragraph()
                if field_type == Date:
                    vals[field] = fpy.date.date(
                        past=True, min_delta=100, max_delta=4000).strftime('%Y-%m-%d')
                if field_type == fields.Boolean:
                    #vals[field] = fpy.basic.random.choice([1, 0])
                    vals[field] = 1

    return test_data
