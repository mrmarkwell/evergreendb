"""Model the EvergreenDB"""

from app import db

# ------------------ Entities ------------------

class Child(db.Model):
    __tablename__ = 'child'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    nickname = db.Column(db.Unicode(255))
    sex = db.Column(db.Unicode(1))
    birth_date = db.Column(db.DateTime)
    abandonment_date = db.Column(db.DateTime)
    program_entry_date = db.Column(db.DateTime)
    program_departure_date = db.Column(db.DateTime)
    program_departure_reason = db.Column(db.UnicodeText)
    child_history = db.Column(db.UnicodeText)
    medical_history = db.Column(db.UnicodeText)
    is_active = db.Column(db.Boolean)
    notes = db.relationship('ChildNote')

    # Association mapping
    partners = db.relationship('ChildPartner', back_populates='child')
    camps = db.relationship('ChildCamp', back_populates='child')
    specialists = db.relationship('ChildAssessment', back_populates='child')
    caregivers = db.relationship('ChildCaregiver', back_populates='child')
    measurement_types = db.relationship('ChildMeasurement', back_populates='child')
    milestone_types = db.relationship('ChildMilestone', back_populates='child')
    doctors = db.relationship('ChildDoctorVisit', back_populates='child')
    medical_conditions = db.relationship('ChildMedicalCondition', back_populates='child')
    medications = db.relationship('ChildMedication', back_populates='child')

    def __repr__(self):
        return '<Child %r>' % (self.nickname)


class ChildNote(db.Model):
    __tablename__ = 'child_note'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    note = db.Column(db.UnicodeText)
    flag = db.Column(db.Boolean)
    child = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)


class Partner(db.Model):
    __tablename__ = 'partner'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    email = db.Column(db.Unicode(255))
    address = db.Column(db.Unicode(255))
    phone = db.Column(db.Unicode(255))
    children = db.relationship('ChildPartner', back_populates='partner')

    def __repr__(self):
        return '<Partner %r>' % (self.english_name)


class Caregiver(db.Model):
    __tablename__ = 'caregiver'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildCaregiver', back_populates='caregiver')

    def __repr__(self):
        return '<Caregiver %r>' % (self.english_name)


class Specialist(db.Model):
    __tablename__ = 'specialist'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    specialist_type = db.Column(db.Integer, db.ForeignKey('specialist_type.id'))
    children = db.relationship('ChildAssessment', back_populates='specialist')

    def __repr__(self):
        return '<Specialist %r>' % (self.english_name)


class SpecialistType(db.Model):
    __tablename__ = 'specialist_type'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    specialists = db.relationship('Specialist')

    def __repr__(self):
        return '<Assessment Type %r>' % (self.english_name)


class MilestoneTypeCategory(db.Model):
    __tablename__ = 'milestone_type_category'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    milestone_types = db.relationship('MilestoneType')

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class MilestoneType(db.Model):
    __tablename__ = 'milestone_type'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    milestone_category = db.Column(
        db.Unicode(16),
        db.ForeignKey('milestone_type_category.id')
    )
    children = db.relationship('ChildMilestone', back_populates='milestone_type')

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class DoctorType(db.Model):
    __tablename__ = 'doctor_type'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
#    doctors = db.relationship('Doctor', back_populates='doctor_type')

    def __repr__(self):
        return '<Doctor Type %r>' % (self.english_name)


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    doctor_english_name = db.Column(db.Unicode(255))
    doctor_chinese_name = db.Column(db.Unicode(255))
    doctor_pinyin_name = db.Column(db.Unicode(255))
    facility_english_name = db.Column(db.Unicode(255))
    facility_chinese_name = db.Column(db.Unicode(255))
    facility_pinyin_name = db.Column(db.Unicode(255))
    doctor_type = db.Column(db.Integer, db.ForeignKey('doctor_type.id'))
    children = db.relationship('ChildDoctorVisit', back_populates='doctor')

    def __repr__(self):
        return '<Doctor %r>' % (self.english_name)


class MeasurementType(db.Model):
    __tablename__ = 'measurement_type'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    units = db.Column(db.Unicode(255))
    children = db.relationship('ChildMeasurement', back_populates='measurement_type')

    def __repr__(self):
        return '<Measurement Type %r>' % (self.english_name)


class Camp(db.Model):
    __tablename__ = 'camp'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildCamp', back_populates='camp')


class MedicalCondition(db.Model):
    __tablename__ = 'medical_condition'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildMedicalCondition', back_populates='medical_condition')


class Medication(db.Model):
    __tablename__ = 'medication'
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.Unicode(255))
    chinese_name = db.Column(db.Unicode(255))
    pinyin_name = db.Column(db.Unicode(255))
    milligram_dose = db.Column(db.Float)
    children = db.relationship('ChildMedication', back_populates='medication')

# ------------------ Associations ------------------


class ChildPartner(db.Model):
    __tablename__ = 'child_partner'
    start_date = db.Column(db.DateTime, primary_key=True)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), primary_key=True)
    child = db.relationship('Child', back_populates='partners')
    partner = db.relationship('Partner', back_populates='children')


class ChildCamp(db.Model):
    __tablename__ = 'child_camp'
    date = db.Column(db.DateTime, primary_key=True)
    notes = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    camp_id = db.Column(db.Integer, db.ForeignKey('camp.id'), primary_key=True)
    child = db.relationship('Child', back_populates='camps')
    camp = db.relationship('Camp', back_populates='children')


class ChildAssessment(db.Model):
    __tablename__ = 'child_assessment'
    date = db.Column(db.DateTime, primary_key=True)
    notes = db.Column(db.UnicodeText)
    flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    specialist_id = db.Column(db.Integer, db.ForeignKey('specialist.id'), primary_key=True)
    child = db.relationship('Child', back_populates='specialists')
    specialist = db.relationship('Specialist', back_populates='children')


class ChildCaregiver(db.Model):
    __tablename__ = 'child_caregiver'
    start_date = db.Column(db.DateTime, primary_key=True)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), primary_key=True)
    child = db.relationship('Child', back_populates='caregivers')
    caregiver = db.relationship('Caregiver', back_populates='children')


class ChildMeasurement(db.Model):
    __tablename__ = 'child_measurement'
    date = db.Column(db.DateTime, primary_key=True)
    value = db.Column(db.Float)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    measurement_type_id = db.Column(db.Integer, db.ForeignKey('measurement_type.id'), primary_key=True)
    child = db.relationship('Child', back_populates='measurement_types')
    measurement_type = db.relationship('MeasurementType', back_populates='children')


class ChildMilestone(db.Model):
    __tablename__ = 'child_milestone'
    date = db.Column(db.DateTime)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    milestone_type_id = db.Column(db.Integer, db.ForeignKey('milestone_type.id'), primary_key=True)
    child = db.relationship('Child', back_populates='milestone_types')
    milestone_type = db.relationship('MilestoneType', back_populates='children')


class ChildDoctorVisit(db.Model):
    __tablename__ = 'child_doctor_visit'
    date = db.Column(db.DateTime, primary_key=True)
    notes = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), primary_key=True)
    child = db.relationship('Child', back_populates='doctors')
    doctor = db.relationship('Doctor', back_populates='children')

class ChildMedicalCondition(db.Model):
    __tablename__ = 'child_medical_condition'
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    medical_condition_id = db.Column(db.Integer, db.ForeignKey('medical_condition.id'), primary_key=True)
    child = db.relationship('Child', back_populates='medical_conditions')
    medical_condition = db.relationship('MedicalCondition', back_populates='children')


class ChildMedication(db.Model):
    __tablename__ = 'child_medication'
    is_active = db.Column(db.Boolean)
    start_date = db.Column(db.DateTime, primary_key=True)
    end_date = db.Column(db.DateTime)
    dosage1 = db.Column(db.Float)
    dosage2 = db.Column(db.Float)
    dosage3 = db.Column(db.Float)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), primary_key=True)
    child = db.relationship('Child', back_populates='medications')
    medication = db.relationship('Medication', back_populates='children')
