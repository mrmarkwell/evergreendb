from flask_restful import fields
class Date(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')

################ Marshallers ####################

base_fields = {
    'id': fields.Integer,
    'english_name': fields.String,
    'chinese_name': fields.String,
    'pinyin_name': fields.String,
    }
child_fields = base_fields.copy()
child_fields.update({
    'nickname': fields.String,
    'sex': fields.String,
    'birth_date': Date,
    'abandonment_date': Date,
    'program_entry_date': Date,
    'program_departure_date': Date,
    'program_departure_reason': fields.String,
    'child_history': fields.String,
    'medical_history': fields.String,
})
child_note_fields = {
    'id': fields.Integer,
    'date': Date,
    'note': fields.String,
    'flag': fields.Boolean,
    'child_id': fields.Integer,
}
partner_fields = base_fields.copy()
partner_fields.update({'email': fields.String, 'phone': fields.String })
caregiver_fields = base_fields.copy()
specialist_fields = base_fields.copy()
specialist_fields.update({'specialist_type_id': fields.Integer})
specialist_type_fields = base_fields.copy()
milestone_type_category_fields = base_fields.copy()
milestone_type_fields = base_fields.copy()
milestone_type_fields.update({'milestone_category': fields.String})
doctor_type_fields = base_fields.copy()
doctor_fields = {
    'id': fields.Integer,
    'doctor_english_name':   fields.String,
    'doctor_chinese_name':   fields.String,
    'doctor_pinyin_name':    fields.String,
    'facility_english_name': fields.String,
    'facility_chinese_name': fields.String,
    'facility_pinyin_name':  fields.String,
    'doctor_type_id': fields.Integer
    }
measurement_type_fields = base_fields.copy()
measurement_type_fields.update({'units': fields.String})

camp_fields = base_fields.copy()
medical_condition_fields = base_fields.copy()
medication_fields = base_fields.copy()
medication_fields.update({'milligram_dose': fields.Float})


child_partner_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'note': fields.String,
    'flag': fields.Boolean,
    'child_id': fields.Integer,
    'partner_id': fields.Integer
}

child_camp_fields = {
    'id': fields.Integer,
    'date': Date,
    'note': fields.String,
    'child_id': fields.Integer,
    'camp_id': fields.Integer
    }

child_assessment_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'note': fields.String,
    'flag': fields.Boolean,
    'specialist_id':fields.Integer
    }

child_caregiver_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'note': fields.String,
    'child_id': fields.Integer,
    'caregiver_id': fields.Integer
    }

child_measurement_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'value': fields.Float,
    'measurement_type_id': fields.Integer
    }

child_milestone_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'milestone_type_id': fields.Integer
    }

child_doctor_visit_fields = {
    'id': fields.Integer,
    'date': Date,
    'child_id': fields.Integer,
    'note': fields.String,
    'doctor_id': fields.Integer
    }

child_medical_condition_fields = {
    'id': fields.Integer,
    'child_id': fields.Integer,
    'medical_condition_id': fields.Integer
    }

child_medication_fields = {
    'id': fields.Integer,
    'start_date': Date,
    'end_date': Date,
    'child_id': fields.Integer,
    'medication_id': fields.Integer,
    'dosage1': fields.Float,
    'dosage2': fields.Float,
    'dosage3': fields.Float
    }
