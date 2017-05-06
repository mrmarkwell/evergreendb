from app import db


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

    def __repr__(self):
        return '<Child %r>' % (self.nickname)


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def __repr__(self):
        return '<Partner %r>' % (self.english_name)


class Specialist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    assessment_specialty = db.Column(db.String(255))

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

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)


class MilestoneType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_name = db.Column(db.String(255))
    chinese_name = db.Column(db.String(255))
    pinyin_name = db.Column(db.String(255))
    milestone_category = db.Column(db.String(16))                                  # ???????????????

    def __repr__(self):
        return '<Milestone Type Category %r>' % (self.english_name)
