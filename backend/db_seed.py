# -*- coding: utf-8 -*-
from tests.rest_test_data import get_test_data
from app import app, db
from production_seed_data import * 
from app.models import MedicalCondition, DoctorType, Medication, MeasurementType
from app.models import MilestoneTypeCategory, MilestoneType, SpecialistType, Camp 
import sys
from pprint import pprint as pp

num_records = 10
test = False
if len(sys.argv) > 1:
    test = bool(sys.argv[1])
if len(sys.argv) > 2:
    num_records = int(sys.argv[2])


custom_seed_tables = ["user", "medical_condition", "doctor_type", "medication", "measurement_type",
                      "milestone_type_category", "milestone_type", "specialist_type", "camp", "fss_medical_condition"]

session = db.session
test_data = get_test_data(num_records)
client = app.test_client()

# Custom seed with realistic data
for condition_name in medical_conditions:
    mc = MedicalCondition()
    print "adding " + mc.__tablename__
    mc.medical_condition_english_name = condition_name
    mc.medical_condition_chinese_name = condition_name
    mc.medical_condition_pinyin_name = condition_name
    session.add(mc)
    session.commit()

for medication in medications:
    m = Medication()
    print "adding " + m.__tablename__
    m.medication_english_name = medication[0]
    m.medication_pinyin_name = medication[0]
    m.medication_chinese_name = medication[1]
    m.milligram_dose = medication[2]
    session.add(m)
    session.commit()

for measurement in measurements:
    m = MeasurementType()
    print "adding " + m.__tablename__
    m.measurement_type_english_name = measurement[0]
    m.measurement_type_chinese_name = measurement[0]
    m.measurement_type_pinyin_name = measurement[0]
    m.units = measurement[1]
    session.add(m)
    session.commit()

for doctor_type in doctor_types:
    dt = DoctorType()
    print "adding " + dt.__tablename__
    dt.doctor_type_english_name = doctor_type
    dt.doctor_type_pinyin_name = doctor_type
    dt.doctor_type_chinese_name = doctor_type
    session.add(dt)
    session.commit()

for mtypecat in milestone_type_categories:
    mtc = MilestoneTypeCategory()
    print "adding " + mtc.__tablename__
    mtc.milestone_type_category_english_name = mtypecat
    mtc.milestone_type_category_pinyin_name = mtypecat
    mtc.milestone_type_category_chinese_name = mtypecat
    session.add(mtc)
    session.commit()

for mtype in milestone_types:
    mt = MilestoneType()
    print "adding " + mt.__tablename__
    mt.milestone_type_english_name = mtype[0]
    mt.milestone_type_pinyin_name = mtype[0]
    mt.milestone_type_chinese_name = mtype[0]
    mt.milestone_type_category_id = mtype[1]
    session.add(mt)
    session.commit()

for stype in specialist_types:
    st = SpecialistType()
    print "adding " + st.__tablename__
    st.specialist_type_english_name = stype
    st.specialist_type_pinyin_name = stype
    st.specialist_type_chinese_name = stype
    session.add(st)
    session.commit()

for camp in camps:
    c = Camp()
    print "adding " + c.__tablename__
    c.camp_english_name = camp
    c.camp_chinese_name = camp
    c.camp_pinyin_name = camp
    session.add(c)
    session.commit()

# Auto seed with fake data
if (test):
    autoseed_list = [key for key in test_data.keys(
    ) if key not in custom_seed_tables]
    for entity in autoseed_list:
        for data in test_data[entity]:
            print "adding " + entity
            response = client.post('/entity/' + entity, data=data)
            if response.status_code != 201:
                print "Something bad happened during DB seed! Attempting a rollback..."
                pp(response.status)
                pp(data)
                session.rollback()
