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
        return '<%r; %r>' % (self.nickname, self.id)
