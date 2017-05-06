"""Model the EvergreenDB"""

from app import db

# ------------------ Entities ------------------

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    sex = db.Column(db.String(1))
    birth_date = db.Column(db.DateTime)
    photo = db.Column(db.LargeBinary)
    abandonment_date = db.Column(db.DateTime)
    program_entry_date = db.Column(db.DateTime)
    program_departure_date = db.Column(db.DateTime)
    program_departure_reason = db.Column(db.Text)
    child_history = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    is_active = db.Column(db.Boolean)
    notes = db.relationship('ChildNote', back_populates='child', lazy='dynamic')

    # Association mapping
    partners = db.relationship('ChildPartner', back_populates='child', lazy='dynamic')
    camps = db.relationship('ChildCamp', back_populates='child', lazy='dynamic')
    assessments = db.relationship('ChildAssessment', back_populates='child', lazy='dynamic')
    caregivers = db.relationship('ChildCaregiver', back_populates='child', lazy='dynamic')
    measurement_types = db.relationship('ChildMeasurement', back_populates='child', lazy='dynamic')
    milestone_types = db.relationship('ChildMilestone', back_populates='child', lazy='dynamic')
    doctors = db.relationship('Doctor', back_populates='child', lazy='dynamic')

    def __repr__(self):
        return '<Child %r>' % (self.nickname)


class ChildNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    note = db.Column(db.Text)
    flag = db.Column(db.Boolean)
    child = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    children = db.relationship('ChildPartner', back_populates='partner', lazy='dynamic')

    def __repr__(self):
        return '<Partner %r>' % (self.english_name)


class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    children = db.relationship('ChildPartner', back_populates='partner', lazy='dynamic')

    def __repr__(self):
        return '<Caregiver %r>' % (self.english_name)


class Specialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    assessment_specialty = db.Column(db.String(255))
    children = db.relationship('ChildAssessment', back_populates='specialist', lazy='dynamic')

    def __repr__(self):
        return '<Specialist %r>' % (self.english_name)


class AssessmentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))

    def __repr__(self):
        return '<Assessment Type %r>' % (self.english_name)


class MilestoneTypeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    milestone_types = db.relationship('MilestoneType', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class MilestoneType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    milestone_category = db.Column(
        db.String(16),
        db.ForeignKey('milestone_category.id')
    )
    children = db.relationship('ChildMilestone', back_populates='milestone_type', lazy='dynamic')

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class DoctorType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    doctors = db.relationship('Doctor', back_populates='type', lazy='dynamic')

    def __repr__(self):
        return '<Doctor Type %r>' % (self.english_name)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_english_name = db.Column(db.String(255))
    doctor_chinese_name = db.Column(db.String(255))
    doctor_pinyin_name = db.Column(db.String(255))
    facility_english_name = db.Column(db.String(255))
    facility_chinese_name = db.Column(db.String(255))
    facility_pinyin_name = db.Column(db.String(255))
    doctor_type = db.Column(db.Integer, db.ForeignKey('doctor_type.id'))
    children = db.relationship('Doctor', back_populates='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Doctor %r>' % (self.english_name)


class MeasurementType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    units = db.Column(db.String(255))
    child_measurements = db.relationship(
        'ChildMeasurement',
        back_populates='measurement_type',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Measurement Type %r>' % (self.english_name)


class CareGiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))


class Camp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    children = db.relationship('ChildCamp', back_populates='camp', lazy='dynamic')


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    milligram_dose = db.Column(db.Float)


class MedicalCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))

# ------------------ Associations ------------------


class ChildPartner(db.Model):
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), primary_key=True)
    child = db.relationship('Child', back_populates='partners', lazy='dynamic')
    partner = db.relationship('Partner', back_populates='children', lazy='dynamic')


class ChildCamp(db.Model):
    date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    camp_id = db.Column(db.Integer, db.ForeignKey('camp.id'), primary_key=True)
    child = db.relationship('Child', back_populates='camps', lazy='dynamic')
    camp = db.relationship('Camp', back_populates='children', lazy='dynamic')


class ChildAssessment(db.Model):
    date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), primary_key=True)
    specialist_id = db.Column(db.Integer, db.ForeignKey('specialist.id'), primary_key=True)
    child = db.relationship('Child', back_populates='specialist', lazy='dynamic')
    specialist = db.relationship('Specialist', back_populates='children', lazy='dynamic')


class ChildCaregiver(db.Model):
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
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
    notes = db.Column(db.Text)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('milestone_type.id'))
    child = db.relationship('Child', back_populates='doctors', lazy='dynamic')
    doctor = db.relationship('Doctor', back_populates='children', lazy='dynamic')
