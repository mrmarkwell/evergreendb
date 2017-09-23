"""Model the EvergreenDB"""

from app import db
from sqlalchemy import UniqueConstraint
from security import pwd_context
from flask_login import UserMixin

########## FSS Tables ##############


class FSSChild(db.Model):
    __tablename__ = 'fss_child'
    __bind_key__ = 'fss'

    # General information
    id = db.Column(db.Integer, primary_key=True)    
    child_english_name = db.Column(db.Unicode(255))
    child_chinese_name = db.Column(db.Unicode(255))
    child_pinyin_name = db.Column(db.Unicode(255))
    nickname = db.Column(db.Unicode(255))
    gender = db.Column(db.Unicode(1))
    birth_date = db.Column(db.DateTime)
    referred_by = db.Column(db.Unicode(255))
    # This can ONLY have values ACTIVE, CURRENT, IN SITU, or RESOLVED.
    status = db.Column(db.Unicode(255))

    # Medical information tab
    primary_diagnosis = db.Column(db.Unicode(255)) # Enum
    primary_diagnosis_note = db.Column(db.Unicode(255))
    secondary_diagnosis = db.Column(db.Unicode(255)) # Enum
    secondary_diagnosis_note = db.Column(db.Unicode(255))
    further_diagnosis = db.Column(db.Unicode(255))
    reason_for_referral = db.Column(db.Unicode(255))
    birth_history = db.Column(db.Unicode(255))
    medical_history = db.Column(db.Unicode(255))

    family_members = db.relationship('FSSFamilyMember', backref='child')
    projceted_pathway = db.relationship('FSSProjectedPathway', backref='child')


class FSSFamilyMember(db.Model):
    __tablename__ = 'fss_family_member'
    __bind_key__ = 'fss'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('fss_child.id'))
    relationship = db.Column(db.Unicode(255))
    family_member_name = db.Column(db.Unicode(255))
    family_member_phone = db.Column(db.Unicode(255))
    family_member_email = db.Column(db.Unicode(255))
    family_member_wechat = db.Column(db.Unicode(255))
    family_member_address = db.Column(db.Unicode(255))
    family_member_notes = db.Column(db.Unicode(255))

class FSSProjectedPathway(db.Model):
    __tablename__ = 'fss_projected_pathway'
    __bind_key__ = 'fss'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('fss_child.id'))
    pathway_step_number = db.Column(db.Integer())
    pathway_short_description = db.Column(db.Unicode(255))
    pathway_details = db.Column(db.Unicode(255))
    pathway_completion_date = db.Column(db.DateTime)

class FSSInteraction(db.Model):
    __tablename__ = 'fss_interaction'
    __bind_key__ = 'fss'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('fss_child.id'))
    interaction_date = db.Column(db.DateTime)
    interaction_type = db.Column(db.Unicode(255))
    interaction_coordinator = db.Column(db.Unicode(255)) # Enum
    people_present = db.Column(db.Unicode(255))
    is_initial_interaction = db.Column(db.Boolean)
    current_concerns = db.Column(db.Unicode(255))
    dev_history = db.Column(db.Unicode(255))
    dev_since_last_visit = db.Column(db.Unicode(255))
    follow_up = db.Column(db.Unicode(255))
    interaction_notes = db.Column(db.Unicode(255))

    milk_feeding = db.Column(db.Boolean)
    solid_feeding = db.Column(db.Boolean)
    self_feeding = db.Column(db.Boolean)
    texture_preferences = db.Column(db.Unicode(255))
    feeding_recommendations = db.Column(db.Unicode(255))
    developmental_notes = db.Column(db.Unicode(255))
    developmental_recommendations = db.Column(db.Unicode(255))
    ot_notes = db.Column(db.Unicode(255))
    ot_recommendations = db.Column(db.Unicode(255))
    sensory_notes = db.Column(db.Unicode(255))
    sensory_recommendations = db.Column(db.Unicode(255))
    speech_notes = db.Column(db.Unicode(255))
    speech_recommendations = db.Column(db.Unicode(255))
    head_control = db.Column(db.Boolean)
    rolling = db.Column(db.Boolean)
    sitting = db.Column(db.Boolean)
    standing = db.Column(db.Boolean)
    walking = db.Column(db.Boolean)
    physical_recommendations = db.Column(db.Unicode(255))
    gross_motor_notes = db.Column(db.Unicode(255))
    gross_motor_recommendations = db.Column(db.Unicode(255))
    fine_motor_notes = db.Column(db.Unicode(255))
    fine_motor_recommendations = db.Column(db.Unicode(255))
    weakness_notes = db.Column(db.Unicode(255))
    weakness_recommendations = db.Column(db.Unicode(255))

########## SOAR Tables #############

# ------------------ Entities ------------------

class Child(db.Model):
    __tablename__ = 'child'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_english_name = db.Column(db.Unicode(255))
    child_chinese_name = db.Column(db.Unicode(255))
    child_pinyin_name = db.Column(db.Unicode(255))
    nickname = db.Column(db.Unicode(255))
    sex = db.Column(db.Unicode(1))
    birth_date = db.Column(db.DateTime)
    abandonment_date = db.Column(db.DateTime)
    program_entry_date = db.Column(db.DateTime)
    program_departure_date = db.Column(db.DateTime)
    program_departure_reason = db.Column(db.UnicodeText)
    child_history = db.Column(db.UnicodeText)
    medical_history = db.Column(db.UnicodeText)
    child_notes = db.relationship('ChildNote')

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

    def __unicode__(self):
        return self.child_english_name


class ChildNote(db.Model):
    __tablename__ = 'child_note'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_note_date = db.Column(db.DateTime)
    child_note = db.Column(db.UnicodeText)
    child_note_flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))


class Partner(db.Model):
    __tablename__ = 'partner'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    partner_english_name = db.Column(db.Unicode(255))
    partner_chinese_name = db.Column(db.Unicode(255))
    partner_pinyin_name = db.Column(db.Unicode(255))
    email = db.Column(db.Unicode(255))
    address = db.Column(db.Unicode(255))
    phone = db.Column(db.Unicode(255))
    children = db.relationship('ChildPartner', back_populates='partner')

    def __unicode__(self):
        return self.partner_english_name

class Caregiver(db.Model):
    __tablename__ = 'caregiver'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    caregiver_english_name = db.Column(db.Unicode(255))
    caregiver_chinese_name = db.Column(db.Unicode(255))
    caregiver_pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildCaregiver', back_populates='caregiver')

    def __repr__(self):
        return '<Caregiver %r>' % (self.english_name)


class Specialist(db.Model):
    __tablename__ = 'specialist'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    specialist_english_name = db.Column(db.Unicode(255))
    specialist_chinese_name = db.Column(db.Unicode(255))
    specialist_pinyin_name = db.Column(db.Unicode(255))
    specialist_type_id = db.Column(db.Integer, db.ForeignKey('specialist_type.id'))
    children = db.relationship('ChildAssessment', back_populates='specialist')

    def __unicode__(self):
        return self.specialist_english_name


class SpecialistType(db.Model):
    __tablename__ = 'specialist_type'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    specialist_type_english_name = db.Column(db.Unicode(255))
    specialist_type_chinese_name = db.Column(db.Unicode(255))
    specialist_type_pinyin_name = db.Column(db.Unicode(255))
    specialists = db.relationship('Specialist', backref='specialist_type')

    def __unicode__(self):
        return self.specialist_type_english_name


class MilestoneTypeCategory(db.Model):
    __tablename__ = 'milestone_type_category'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    milestone_type_category_english_name = db.Column(db.Unicode(255))
    milestone_type_category_chinese_name = db.Column(db.Unicode(255))
    milestone_type_category_pinyin_name = db.Column(db.Unicode(255))
    milestone_types = db.relationship('MilestoneType', backref='milestone_type_category')

    def __unicode__(self):
        return self.milestone_type_category_english_name

class MilestoneType(db.Model):
    __tablename__ = 'milestone_type'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    milestone_type_english_name = db.Column(db.Unicode(255))
    milestone_type_chinese_name = db.Column(db.Unicode(255))
    milestone_type_pinyin_name = db.Column(db.Unicode(255))
    milestone_type_category_id = db.Column(
        db.Unicode(16),
        db.ForeignKey('milestone_type_category.id')
    )
    children = db.relationship('ChildMilestone', back_populates='milestone_type')

    def __unicode__(self):
        return self.milestone_type_english_name

class DoctorType(db.Model):
    __tablename__ = 'doctor_type'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    doctor_type_english_name = db.Column(db.Unicode(255))
    doctor_type_chinese_name = db.Column(db.Unicode(255))
    doctor_type_pinyin_name = db.Column(db.Unicode(255))
    doctors = db.relationship('Doctor', backref='doctor_type')

    def __unicode__(self):
        return self.doctor_type_english_name

class Doctor(db.Model):
    __tablename__ = 'doctor'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    doctor_english_name = db.Column(db.Unicode(255))
    doctor_chinese_name = db.Column(db.Unicode(255))
    doctor_pinyin_name = db.Column(db.Unicode(255))
    facility_english_name = db.Column(db.Unicode(255))
    facility_chinese_name = db.Column(db.Unicode(255))
    facility_pinyin_name = db.Column(db.Unicode(255))
    doctor_type_id = db.Column(db.Integer, db.ForeignKey('doctor_type.id'))
    children = db.relationship('ChildDoctorVisit', back_populates='doctor')

    def __unicode__(self):
        return self.doctor_english_name

class MeasurementType(db.Model):
    __tablename__ = 'measurement_type'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    measurement_type_english_name = db.Column(db.Unicode(255))
    measurement_type_chinese_name = db.Column(db.Unicode(255))
    measurement_type_pinyin_name = db.Column(db.Unicode(255))
    units = db.Column(db.Unicode(255))
    children = db.relationship('ChildMeasurement', back_populates='measurement_type')

    def __unicode__(self):
        return self.measurement_type_english_name


class Camp(db.Model):
    __tablename__ = 'camp'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    camp_english_name = db.Column(db.Unicode(255))
    camp_chinese_name = db.Column(db.Unicode(255))
    camp_pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildCamp', back_populates='camp')
    def __unicode__(self):
        return self.camp_english_name

class MedicalCondition(db.Model):
    __tablename__ = 'medical_condition'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    medical_condition_english_name = db.Column(db.Unicode(255))
    medical_condition_chinese_name = db.Column(db.Unicode(255))
    medical_condition_pinyin_name = db.Column(db.Unicode(255))
    children = db.relationship('ChildMedicalCondition', back_populates='medical_condition')

    def __unicode__(self):
        return self.medical_condition_english_name

class Medication(db.Model):
    __tablename__ = 'medication'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    medication_english_name = db.Column(db.Unicode(255))
    medication_chinese_name = db.Column(db.Unicode(255))
    medication_pinyin_name = db.Column(db.Unicode(255))
    milligram_dose = db.Column(db.Float)
    children = db.relationship('ChildMedication', back_populates='medication')

    def __unicode__(self):
        return self.medication_english_name
# ------------------ Associations ------------------


class ChildPartner(db.Model):
    __tablename__ = 'child_partner'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_partner_start_date = db.Column(db.DateTime)
    child_partner_end_date = db.Column(db.DateTime)
    child_partner_note = db.Column(db.UnicodeText)
    child_partner_note_flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    child = db.relationship('Child', back_populates='partners')
    partner = db.relationship('Partner', back_populates='children')
    __table_args__ = (UniqueConstraint('child_id', 'partner_id', 'child_partner_start_date'),)

    def __unicode__(self):
        p = Partner.query.get(self.partner_id);
        c = Child.query.get(self.child_id);
        return "CHILD: '" + c.child_english_name + "' PARTNER: '" + p.partner_english_name + "'"


class ChildCamp(db.Model):
    __tablename__ = 'child_camp'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_camp_date = db.Column(db.DateTime)
    child_camp_note = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    camp_id = db.Column(db.Integer, db.ForeignKey('camp.id'))
    child = db.relationship('Child', back_populates='camps')
    camp = db.relationship('Camp', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'camp_id', 'child_camp_date'),)

class ChildAssessment(db.Model):
    __tablename__ = 'child_assessment'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_assessment_date = db.Column(db.DateTime)
    child_assessment_note = db.Column(db.UnicodeText)
    child_assessment_note_flag = db.Column(db.Boolean)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    specialist_id = db.Column(db.Integer, db.ForeignKey('specialist.id'))
    child = db.relationship('Child', back_populates='specialists')
    specialist = db.relationship('Specialist', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'specialist_id', 'child_assessment_date'),)

class ChildCaregiver(db.Model):
    __tablename__ = 'child_caregiver'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_caregiver_start_date = db.Column(db.DateTime)
    child_caregiver_end_date = db.Column(db.DateTime)
    child_caregiver_note = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'))
    child = db.relationship('Child', back_populates='caregivers')
    caregiver = db.relationship('Caregiver', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'caregiver_id', 'child_caregiver_start_date'),)

class ChildMeasurement(db.Model):
    __tablename__ = 'child_measurement'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_measurement_date = db.Column(db.DateTime)
    child_measurement_value = db.Column(db.Float)
    child_measurement_comment = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    measurement_type_id = db.Column(db.Integer, db.ForeignKey('measurement_type.id'))
    child = db.relationship('Child', back_populates='measurement_types')
    measurement_type = db.relationship('MeasurementType', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'measurement_type_id', 'child_measurement_date'),)

class ChildMilestone(db.Model):
    __tablename__ = 'child_milestone'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_milestone_date = db.Column(db.DateTime)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    milestone_type_id = db.Column(db.Integer, db.ForeignKey('milestone_type.id'))
    child = db.relationship('Child', back_populates='milestone_types')
    milestone_type = db.relationship('MilestoneType', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'milestone_type_id'),)

class ChildDoctorVisit(db.Model):
    __tablename__ = 'child_doctor_visit'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_doctor_visit_date = db.Column(db.DateTime)
    child_doctor_visit_note = db.Column(db.UnicodeText)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    child = db.relationship('Child', back_populates='doctors')
    doctor = db.relationship('Doctor', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'doctor_id', 'child_doctor_visit_date'),)

class ChildMedicalCondition(db.Model):
    __tablename__ = 'child_medical_condition'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    medical_condition_id = db.Column(db.Integer, db.ForeignKey('medical_condition.id'))
    child = db.relationship('Child', back_populates='medical_conditions')
    medical_condition = db.relationship('MedicalCondition', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'medical_condition_id'),)

class ChildMedication(db.Model):
    __tablename__ = 'child_medication'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    child_medication_start_date = db.Column(db.DateTime)
    child_medication_end_date = db.Column(db.DateTime)
    dosage1 = db.Column(db.Float)
    dosage2 = db.Column(db.Float)
    dosage3 = db.Column(db.Float)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'))
    child = db.relationship('Child', back_populates='medications')
    medication = db.relationship('Medication', back_populates='children')

    __table_args__ = (UniqueConstraint('child_id', 'medication_id', 'child_medication_start_date'),)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __bind_key__ = 'soar'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), unique=True, index=True)
    password_hash = db.Column(db.Unicode(255))
    is_admin = db.Column(db.Boolean(), default=False)
    is_editor = db.Column(db.Boolean(), default=False)
    #email = db.Column(db.Unicode(255))
    #created = db.Column(db.DateTime)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return unicode(self.id)

