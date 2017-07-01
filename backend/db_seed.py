# -*- coding: utf-8 -*-
from tests.rest_test_data import get_test_data
from app import app, db
from app.models import MedicalCondition, DoctorType, Medication, MeasurementType
from app.models import MilestoneTypeCategory, MilestoneType, SpecialistType, Camp
import sys

num_records = 10
if len(sys.argv) > 1:
    num_records = int(sys.argv[1])

custom_seed_tables = ["user", "medical_condition", "doctor_type", "medication", "measurement_type",
                      "milestone_type_category", "milestone_type", "specialist_type", "camp", "fss_child"]

medical_conditions = [
    u"CP",
    u"Autism",
    u"Intellectual Disability",
    u"ADHD",
    u"Lennox-Gastaut",
    u"Angelman Syndrome",
    u"PKU",
    u"Cleft Lip / Cleft Palate",
    u"Hepatitis B"]

medications = [
    (u"Carbamazepine", u"卡马西平", 100),
    (u"Lamotrigine", u"拉莫三嗪", 50),
    (u"Phenobarbital", u"苯巴比妥", 30),
    (u"Topiramate", u"妥泰", 25),
    (u"Valproate", u"丙戊酸钠", 200),
    (u"Haloperidol", u"氟哌啶醇", 2),
    (u"Quetiapine", u"富马酸喹硫平", 100),
    (u"Risperidone", u"利培酮", 1)]

measurements = [
    (u"weight", u"kg"),
    (u"height", u"cm"),
    (u"MUAC", u"cm"),
    (u"Head Circumference", u"cm")]

doctor_types = [
    u"Paediatrician",
    u"Neurologist",
    u"Dentist",
    u"OT",
    u"PT",
    u"Ophthalmologist",
    u"EG Doctor"]

milestone_type_categories = [
    u"Communication Milestones",
    u"Physical Milestones",
    u"Life Skills"]

# Since milestone type categories are seeded in the order above,
# the second element of the below tuples is the id of the category.
milestone_types = [
    (u"Vocalizes", 1),
    (u"Responds to name", 1),
    (u"Says 2-3 words", 1),
    (u"Says several words", 1),
    (u"Says sentences containing subject & verb", 1),
    (u"Converses in sentences", 1),
    (u"Can count", 1),
    (u"Reached", 2),
    (u"Date", 2),
    (u"Sits alone", 2),
    (u"Crawls", 2),
    (u"Stands alone", 2),
    (u"Walks with assistance", 2),
    (u"Walks alone", 2),
    (u"Reached", 3),
    (u"Date", 3),
    (u"Uses simple gestures (i.e. bye-bye, shakes head)", 3),
    (u"Drinks from a cup", 3),
    (u"Eats with a spoon", 3),
    (u"Toilet trained", 3),
    (u"Scribbles", 3),
    (u"Copies shapes", 3)]

specialist_types = [
    u"OT",
    u"PT",
    u"SLP",
    u"PSY"]

camps = [
    u"Bring me Hope",
    u"Bridge of Hope",
    u"Joy in the Journey"]

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
autoseed_list = [key for key in test_data.keys(
) if key not in custom_seed_tables]
for entity in autoseed_list:
    for data in test_data[entity]:
        print "adding " + entity
        response = client.post('/entity/' + entity, data=data)
        if response.status_code != 201:
            print "Something bad happened during DB seed! Attempting a rollback..."
            session.rollback()
