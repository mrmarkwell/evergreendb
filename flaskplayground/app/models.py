"""Model the EvergreenDB"""

from app import db

# ------------------ Entities ------------------

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    nickname = db.Column(db.Unicode(255))
    sex = db.Column(db.Unicode(1))
    birth_date = db.Column(db.DateTime)
    photo = db.Column(db.LargeBinary)
    abandonment_date = db.Column(db.DateTime)
    program_entry_date = db.Column(db.DateTime)
    program_departure_date = db.Column(db.DateTime)
    program_departure_reason = db.Column(db.UnicodeText)
    child_history = db.Column(db.UnicodeText)
    medical_history = db.Column(db.UnicodeText)
    is_active = db.Column(db.Boolean)
    notes = db.relationship('ChildNote', back_populates='child', lazy='dynamic')

    # Association mapping
    partners = db.relationship('ChildPartner', back_populates='child', lazy='dynamic')
    camps = db.relationship('ChildCamp', back_populates='child', lazy='dynamic')
    assessments = db.relationship('ChildAssessment', back_populates='child', lazy='dynamic')
    caregivers = db.relationship('ChildCaregiver', back_populates='child', lazy='dynamic')
    measurement_types = db.relationship('ChildMeasurement', back_populates='child', lazy='dynamic')
    milestone_types = db.relationship('ChildMilestone', back_populates='child', lazy='dynamic')
    doctors = db.relationship('ChildDoctorVisit', back_populates='child', lazy='dynamic')
    medical_conditions = db.relationship('ChildMedicalCondition', back_populates='child', lazy='dynamic')
    medications = db.relationship('ChildMedication', back_populates='child', lazy='dynamic')

    def __repr__(self):
        return '<Child %r>' % (self.nickname)


class ChildNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    note = db.Column(db.UnicodeText)
    flag = db.Column(db.Boolean)
    child = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    email = db.Column(db.Unicode(255))
    address = db.Column(db.Unicode(255))
    phone = db.Column(db.Unicode(255))
    children = db.relationship('ChildPartner', back_populates='partner', lazy='dynamic')

    def __repr__(self):
        return '<Partner %r>' % (self.english_name)


class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildPartner', back_populates='partner', lazy='dynamic')

    def __repr__(self):
        return '<Caregiver %r>' % (self.english_name)


class Specialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    specialist_type_id = db.Column(db.Integer, db.ForeignKey('specialist_type.id'))
    children = db.relationship('ChildAssessment', back_populates='specialist', lazy='dynamic')

    def __repr__(self):
        return '<Specialist %r>' % (self.english_name)


class SpecialistType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    specialists = db.relationship('Specialist', back_populates='specialist_type', lazy='dynamic')

    def __repr__(self):
        return '<Assessment Type %r>' % (self.english_name)


class MilestoneTypeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    milestone_types = db.relationship('MilestoneType', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class MilestoneType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    milestone_category = db.Column(
        db.Unicode(16),
        db.ForeignKey('milestone_category.id')
    )
    children = db.relationship('ChildMilestone', back_populates='milestone_type', lazy='dynamic')

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class DoctorType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    doctors = db.relationship('Doctor', back_populates='type', lazy='dynamic')

    def __repr__(self):
        return '<Doctor Type %r>' % (self.english_name)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_english_name = db.Column(db.Unicode(255))
    doctor_chinese_name = db.Column(db.Unicode(255))
    doctor_pinyin_name = db.Column(db.Unicode(255))
    facility_english_name = db.Column(db.Unicode(255))
    facility_chinese_name = db.Column(db.Unicode(255))
    facility_pinyin_name = db.Column(db.Unicode(255))
    doctor_type = db.Column(db.Integer, db.ForeignKey('doctor_type.id'))
    children = db.relationship('Doctor', back_populates='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Doctor %r>' % (self.english_name)


class MeasurementType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    units = db.Column(db.Unicode(255))
    child_measurements = db.relationship(
        'ChildMeasurement',
        back_populates='measurement_type',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Measurement Type %r>' % (self.english_name)


class Camp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildCamp', back_populates='camp', lazy='dynamic')


class MedicalCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildMedicalCondition', back_populates='medical_condition', lazy='dynamic')


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    milligram_dose = db.Column(db.Float)
    children = db.relationship('ChildMedication', back_populates='medication', lazy='dynamic')

# ------------------ Associations ------------------


class ChildPartner(db.Model):
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), primary_key=True)
    child = db.relationship('Child', back_populates='partners', lazy='dynamic')
    partner = db.relationship('Partner', back_populates='children', lazy='dynamic')


class ChildCamp(db.Model):
    date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    camp_id = db.Column(db.Integer, db.ForeignKey('camp.id'), primary_key=True)
    child = db.relationship('Child', back_populates='camps', lazy='dynamic')
    camp = db.relationship('Camp', back_populates='children', lazy='dynamic')


class ChildAssessment(db.Model):
    date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    specialist_id = db.Column(db.Integer, db.ForeignKey('specialist.id'), primary_key=True)
    child = db.relationship('Child', back_populates='specialist', lazy='dynamic')
    specialist = db.relationship('Specialist', back_populates='children', lazy='dynamic')


class ChildCaregiver(db.Model):
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), primary_key=True)
    child = db.relationship('Child', back_populates='caregivers', lazy='dynamic')
    caregiver = db.relationship('Caregiver', back_populates='children', lazy='dynamic')


class ChildMeasurement(db.Model):
    date = db.Column(db.DateTime)
    value = db.Column(db.Float)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    measurement_type_id = db.Column(db.Integer, db.ForeignKey('measurement_type.id'))
    child = db.relationship('Child', back_populates='measurement_types', lazy='dynamic')
    measurement_type = db.relationship('MeasurementType', back_populates='children', lazy='dynamic')


class ChildMilestone(db.Model):
    date = db.Column(db.DateTime)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    milestone_type_id = db.Column(db.Integer, db.ForeignKey('milestone_type.id'))
    child = db.relationship('Child', back_populates='milestone_types', lazy='dynamic')
    milestone_type = db.relationship('MilestoneType', back_populates='children', lazy='dynamic')


class ChildDoctorVisit(db.Model):
    date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    child = db.relationship('Child', back_populates='doctors', lazy='dynamic')
    doctor = db.relationship('Doctor', back_populates='children', lazy='dynamic')

class ChildMedicalCondition(db.Model):
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    medical_condition_id = db.Column(db.Integer, db.ForeignKey('medical_condition.id'))
    child = db.relationship('Child', back_populates='medical_conditions', lazy='dynamic')
    medical_condition = db.relationship('MedicalCondition', back_populates='children', lazy='dynamic')


class ChildMedication(db.Model):
    is_active = db.Column(db.Boolean)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    dosage1 = db.Column(db.Float)
    dosage2 = db.Column(db.Float)
    dosage3 = db.Column(db.Float)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    medication = db.Column(db.Integer, db.ForeignKey('medication.id'))
    child = db.relationship('Child', back_populates='medications', lazy='dynamic')
    medications = db.relationship('MedicalCondition', back_populates='children', lazy='dynamic')
