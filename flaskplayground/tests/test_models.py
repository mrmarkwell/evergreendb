"""Simple tests for our DB Models"""

from datetime import date
import os
import random
import unittest

from app import app, db, models
from config import basedir

C_NAME = unicode(
    "\xe5\x81\x9a\xe6\x88\x8f\xe4\xb9\x8b\xe8\xaf\xb4".decode('utf8'))
P_NAME = unicode('idunnopinyin')
E_NAME = unicode("johnny")
NOTE = unicode("This is a note. It has some long text and is very informative")
FLAG = random.choice([True, False])
TODAY = date.today()


class TestEntityCreation(unittest.TestCase):
    """Simple tests for entity models"""

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def test_entity_creation_child(self):
        child = models.Child(english_name=E_NAME,
                             chinese_name=C_NAME, pinyin_name=P_NAME)
        db.session.add(child)
        db.session.commit()
        children = db.session.query(models.Child).all()
        self.assertTrue(child.id in [_child.id for _child in children])

    def test_entity_creation_child_note(self):
        child_note = models.ChildNote(
            note=NOTE,
            flag=FLAG,
            date=TODAY,
            child=0
        )
        db.session.add(child_note)
        db.session.commit()
        notes = db.session.query(models.ChildNote).all()
        self.assertTrue(child_note.id in [
                        _child_note.id for _child_note in notes])

    def test_entity_creation_partner(self):
        partner = models.Partner(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
            email=unicode('example@example.com')
        )
        db.session.add(partner)
        db.session.commit()
        partners = db.session.query(models.Partner).all()
        self.assertTrue(partner.id in [_partner.id for _partner in partners])

    def test_entity_creation_caregiver(self):
        caregiver = models.Caregiver(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(caregiver)
        db.session.commit()
        caregivers = db.session.query(models.Caregiver).all()
        self.assertEqual(len(caregivers), 1)

    def test_entity_creation_specialist(self):
        specialist = models.Specialist(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(specialist)
        db.session.commit()
        specialists = db.session.query(models.Specialist).all()
        self.assertEqual(len(specialists), 1)

    def test_entity_creation_specialist_type(self):
        specialist_type = models.SpecialistType(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(specialist_type)
        db.session.commit()
        specialist_types = db.session.query(models.SpecialistType).all()
        self.assertEqual(len(specialist_types), 1)

    def test_entity_creation_milestone_type(self):
        milestone_type = models.MilestoneType(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(milestone_type)
        db.session.commit()
        milestone_types = db.session.query(models.MilestoneType).all()
        self.assertEqual(len(milestone_types), 1)

    def test_entity_creation_milestone_type_category(self):
        milestone_type_category = models.MilestoneTypeCategory(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(milestone_type_category)
        db.session.commit()
        milestone_type_categorys = db.session.query(
            models.MilestoneTypeCategory).all()
        self.assertEqual(len(milestone_type_categorys), 1)

    def test_entity_creation_doctor(self):
        doctor = models.Doctor(
            doctor_english_name=E_NAME,
            doctor_chinese_name=C_NAME,
            doctor_pinyin_name=P_NAME,
            facility_english_name=E_NAME,
            facility_chinese_name=C_NAME,
            facility_pinyin_name=P_NAME,
        )
        db.session.add(doctor)
        db.session.commit()
        doctors = db.session.query(models.Doctor).all()
        self.assertEqual(len(doctors), 1)

    def test_entity_creation_doctor_type(self):
        doctor_type = models.DoctorType(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(doctor_type)
        db.session.commit()
        doctor_types = db.session.query(models.DoctorType).all()
        self.assertEqual(len(doctor_types), 1)

    def test_entity_creation_measurement_type(self):
        measurement_type = models.MeasurementType(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(measurement_type)
        db.session.commit()
        measurement_types = db.session.query(models.MeasurementType).all()
        self.assertEqual(len(measurement_types), 1)

    def test_entity_creation_camp(self):
        camp = models.Camp(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(camp)
        db.session.commit()
        camps = db.session.query(models.Camp).all()
        self.assertTrue(camp.id in [_camp.id for _camp in camps])

    def test_entity_creation_medical_condition(self):
        medical_condition = models.MedicalCondition(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(medical_condition)
        db.session.commit()
        medical_conditions = db.session.query(models.MedicalCondition).all()
        self.assertEqual(len(medical_conditions), 1)

    def test_entity_creation_medication(self):
        medication = models.Medication(
            english_name=E_NAME,
            chinese_name=C_NAME,
            pinyin_name=P_NAME,
        )
        db.session.add(medication)
        db.session.commit()
        medications = db.session.query(models.Medication).all()
        self.assertEqual(len(medications), 1)


class TestAssociationCreation(unittest.TestCase):
    """simple test for association table creation"""

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()

        child = models.Child()
        partner = models.Partner()
        camp = models.Camp()
        caregiver = models.Caregiver()
        specialist = models.Specialist()
        measurement = models.MeasurementType()
        milestone = models.MilestoneType()
        doctor = models.Doctor()
        medical_condition = models.MedicalCondition()
        medication = models.Medication()
        db.session.add_all([child, partner, camp, caregiver, specialist,
                            measurement, milestone, doctor, medical_condition,
                            medication])

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def test_association_creation_child_partner(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        partners = db.session.query(models.Partner).all()
        partner = random.choice(partners)
        child_partner = models.ChildPartner(
            start_date=TODAY,
            end_date=TODAY,
            note=NOTE,
            flag=FLAG,
            child_id=child.id,
            partner_id=partner.id
        )
        db.session.add(child_partner)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(partner.id in [_partner.id for _partner in partners])
        child_partners = db.session.query(models.ChildPartner).all()
        self.assertTrue(child_partner.child_id in [
                        _child_partner.child_id for _child_partner in child_partners])
        self.assertTrue(child_partner.partner_id in [
                        _child_partner.partner_id for _child_partner in child_partners])

    def test_association_creation_child_camp(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        camps = db.session.query(models.Camp).all()
        camp = random.choice(camps)
        child_camp = models.ChildCamp(
            date=TODAY,
            note=NOTE,
            child_id=child.id,
            camp_id=camp.id
        )
        db.session.add(child_camp)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(camp.id in [_camp.id for _camp in camps])
        child_camps = db.session.query(models.ChildCamp).all()
        self.assertTrue(child_camp.child_id in [
                        _child_camp.child_id for _child_camp in child_camps])
        self.assertTrue(child_camp.camp_id in [
                        _child_camp.camp_id for _child_camp in child_camps])

    def test_association_creation_child_assessment(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        specialists = db.session.query(models.Specialist).all()
        specialist = random.choice(specialists)
        child_assessment = models.ChildAssessment(
            date=TODAY,
            note=NOTE,
            flag=FLAG,
            child_id=child.id,
            specialist_id=specialist.id
        )
        db.session.add(child_assessment)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(specialist.id in [
                        _specialist.id for _specialist in specialists])
        child_assessments = db.session.query(models.ChildAssessment).all()
        self.assertTrue(child_assessment.child_id in [
                        _child_assessment.child_id for _child_assessment in child_assessments])
        self.assertTrue(child_assessment.specialist_id in [
                        _child_assessment.specialist_id for _child_assessment in child_assessments])

    def test_association_creation_child_caregiver(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        caregivers = db.session.query(models.Caregiver).all()
        caregiver = random.choice(caregivers)
        child_caregiver = models.ChildCaregiver(
            start_date=TODAY,
            end_date=TODAY,
            note=NOTE,
            child_id=child.id,
            caregiver_id=caregiver.id
        )
        db.session.add(child_caregiver)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(caregiver.id in [
                        _caregiver.id for _caregiver in caregivers])
        child_caregivers = db.session.query(models.ChildCaregiver).all()
        self.assertTrue(child_caregiver.child_id in [
                        _child_caregiver.child_id for _child_caregiver in child_caregivers])
        self.assertTrue(child_caregiver.caregiver_id in [
                        _child_caregiver.caregiver_id for _child_assessment in child_caregivers])

    def test_association_creation_child_measurement(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        measurements = db.session.query(models.MeasurementType).all()
        measurement = random.choice(measurements)
        child_measurement = models.ChildMeasurement(
            date=TODAY,
            value=0,
            child_id=child.id,
            measurement_type_id=measurement.id
        )
        db.session.add(child_measurement)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(measurement.id in [
                        _measurement.id for _measurement in measurements])
        child_measurements = db.session.query(models.ChildMeasurement).all()
        self.assertTrue(child_measurement.child_id in [
                        _child_measurement.child_id for _child_measurement in child_measurements])
        self.assertTrue(child_measurement.measurement_type_id in [
                        _child_measurement.measurement_type_id for _child_assessment in child_measurements])

    def test_association_creation_child_milestone(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        milestones = db.session.query(models.MilestoneType).all()
        milestone = random.choice(milestones)
        child_milestone = models.ChildMilestone(
            date=TODAY,
            child_id=child.id,
            milestone_type_id=milestone.id
        )
        db.session.add(child_milestone)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(milestone.id in [
                        _milestone.id for _milestone in milestones])
        child_milestones = db.session.query(models.ChildMilestone).all()
        self.assertTrue(child_milestone.child_id in [
                        _child_milestone.child_id for _child_milestone in child_milestones])
        self.assertTrue(child_milestone.milestone_type_id in [
                        _child_milestone.milestone_type_id for _child_assessment in child_milestones])

    def test_association_creation_child_doctor_visit(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        doctors = db.session.query(models.Doctor).all()
        doctor = random.choice(doctors)
        child_doctor_visit = models.ChildDoctorVisit(
            date=TODAY,
            note=NOTE,
            child_id=child.id,
            doctor_id=doctor.id
        )
        db.session.add(child_doctor_visit)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(doctor.id in [_doctor.id for _doctor in doctors])
        child_doctor_visits = db.session.query(models.ChildDoctorVisit).all()
        self.assertTrue(child_doctor_visit.child_id in [
                        _child_doctor.child_id for _child_doctor in child_doctor_visits])
        self.assertTrue(child_doctor_visit.doctor_id in [
                        _child_doctor.doctor_id for _child_assessment in child_doctor_visits])

    def test_association_creation_child_medical_condition(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        medical_conditions = db.session.query(models.MedicalCondition).all()
        medical_condition = random.choice(medical_conditions)
        child_medical_condition = models.ChildMedicalCondition(
            child_id=child.id,
            medical_condition_id=medical_condition.id
        )
        db.session.add(child_medical_condition)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(medical_condition.id in [
                        _medical_condition.id for _medical_condition in medical_conditions])
        child_medical_conditions = db.session.query(
            models.ChildMedicalCondition).all()
        self.assertTrue(child_medical_condition.child_id in [
                        _child_medical_condition.child_id for _child_medical_condition in child_medical_conditions])
        self.assertTrue(child_medical_condition.medical_condition_id in
                        [_child_medical_condition.medical_condition_id for _child_assessment in
                         child_medical_conditions])

    def test_association_creation_child_medication(self):
        children = db.session.query(models.Child).all()
        child = random.choice(children)
        medications = db.session.query(models.Medication).all()
        medication = random.choice(medications)
        child_medication = models.ChildMedication(
            is_active=FLAG,
            start_date=TODAY,
            end_date=TODAY,
            dosage1=0.0,
            dosage2=0.0,
            dosage3=0.0,
            child_id=child.id,
            medication_id=medication.id
        )
        db.session.add(child_medication)
        db.session.commit()
        self.assertTrue(child.id in [_child.id for _child in children])
        self.assertTrue(medication.id in [
                        _medication.id for _medication in medications])
        child_medications = db.session.query(models.ChildMedication).all()
        self.assertTrue(child_medication.child_id in [
                        _child_medication.child_id for _child_medication in child_medications])
        self.assertTrue(child_medication.medication_id in [
                        _child_medication.medication_id for _child_assessment in child_medications])

if __name__ == '__main__':
    unittest.main()
