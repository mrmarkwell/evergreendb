from flask_restful import fields

DATE_FMT = '%Y-%m-%d'

class Date(fields.Raw):
    def format(self, value):
        return value.strftime(DATE_FMT)

################ Marshallers ####################

#-------------- FSS Marshallers ----------------#

fss_child_fields = {
    'id': fields.Integer,
    'child_english_name': fields.String,
    'child_chinese_name': fields.String,
    'child_pinyin_name': fields.String,
    'nickname': fields.String,
    'gender': fields.String,
    'birth_date': Date,
    'referred_by': fields.String,
    'status': fields.String,
    'primary_diagnosis': fields.String,
    'secondary_diagnosis': fields.String,
    'further_diagnosis': fields.String,
    'reason_for_referral': fields.String,
}

#-------------- SOAR Marshallers ----------------#

child_fields = {
    'id': fields.Integer,
    'child_english_name': fields.String,
    'child_chinese_name': fields.String,
    'child_pinyin_name': fields.String,
    'nickname': fields.String,
    'sex': fields.String,
    'birth_date': Date,
    'abandonment_date': Date,
    'program_entry_date': Date,
    'program_departure_date': Date,
    'program_departure_reason': fields.String,
    'child_history': fields.String,
    'medical_history': fields.String,
}
child_note_fields = {
    'id': fields.Integer,
    'child_note_date': Date,
    'child_note': fields.String,
    'child_note_flag': fields.Boolean,
    'child_id': fields.Integer,
}
partner_fields = {
    'id': fields.Integer,
    'partner_english_name': fields.String,
    'partner_chinese_name': fields.String,
    'partner_pinyin_name': fields.String,
    'email': fields.String,
    'phone': fields.String
}
caregiver_fields = {
    'id': fields.Integer,
    'caregiver_english_name': fields.String,
    'caregiver_chinese_name': fields.String,
    'caregiver_pinyin_name': fields.String
}
specialist_fields = {
    'id': fields.Integer,
    'specialist_english_name': fields.String,
    'specialist_chinese_name': fields.String,
    'specialist_pinyin_name': fields.String,
    'specialist_type_id': fields.Integer
}
specialist_type_fields = {
    'id': fields.Integer,
    'specialist_type_english_name': fields.String,
    'specialist_type_chinese_name': fields.String,
    'specialist_type_pinyin_name': fields.String
}
milestone_type_category_fields = {
    'id': fields.Integer,
    'milestone_type_category_english_name': fields.String,
    'milestone_type_category_chinese_name': fields.String,
    'milestone_type_category_pinyin_name': fields.String
}

milestone_type_fields = {
    'id': fields.Integer,
    'milestone_type_english_name': fields.String,
    'milestone_type_chinese_name': fields.String,
    'milestone_type_pinyin_name': fields.String,
    'milestone_type_category_id': fields.Integer
}

doctor_type_fields = {
    'id': fields.Integer,
    'doctor_type_english_name': fields.String,
    'doctor_type_chinese_name': fields.String,
    'doctor_type_pinyin_name': fields.String
}

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
measurement_type_fields = {
    'id': fields.Integer,
    'measurement_type_english_name': fields.String,
    'measurement_type_chinese_name': fields.String,
    'measurement_type_pinyin_name': fields.String,
    'units': fields.String
}

camp_fields = {
    'id': fields.Integer,
    'camp_english_name':   fields.String,
    'camp_chinese_name':   fields.String,
    'camp_pinyin_name':    fields.String
}
medical_condition_fields = {
    'id': fields.Integer,
    'medical_condition_english_name':   fields.String,
    'medical_condition_chinese_name':   fields.String,
    'medical_condition_pinyin_name':    fields.String
}
medication_fields = {
    'id': fields.Integer,
    'medication_english_name':   fields.String,
    'medication_chinese_name':   fields.String,
    'medication_pinyin_name':    fields.String,
    'milligram_dose': fields.Float
}


child_partner_fields = {
    'id': fields.Integer,
    'child_partner_start_date': Date,
    'child_partner_end_date': Date,
    'child_partner_note': fields.String,
    'child_partner_note_flag': fields.Boolean,
    'child_id': fields.Integer,
    'partner_id': fields.Integer
}

child_camp_fields = {
    'id': fields.Integer,
    'child_camp_date': Date,
    'child_camp_note': fields.String,
    'child_id': fields.Integer,
    'camp_id': fields.Integer
    }

child_assessment_fields = {
    'id': fields.Integer,
    'child_assessment_date': Date,
    'child_id': fields.Integer,
    'child_assessment_note': fields.String,
    'child_assessment_note_flag': fields.Boolean,
    'specialist_id':fields.Integer
    }

child_caregiver_fields = {
    'id': fields.Integer,
    'child_caregiver_start_date': Date,
    'child_caregiver_end_date': Date,
    'child_caregiver_note': fields.String,
    'child_id': fields.Integer,
    'caregiver_id': fields.Integer
    }

child_measurement_fields = {
    'id': fields.Integer,
    'child_measurement_date': Date,
    'child_id': fields.Integer,
    'child_measurement_comment': fields.String,
    'child_measurement_value': fields.Float,
    'measurement_type_id': fields.Integer
    }

child_milestone_fields = {
    'id': fields.Integer,
    'child_milestone_date': Date,
    'child_id': fields.Integer,
    'milestone_type_id': fields.Integer
    }

child_doctor_visit_fields = {
    'id': fields.Integer,
    'child_doctor_visit_date': Date,
    'child_id': fields.Integer,
    'child_doctor_visit_note': fields.String,
    'doctor_id': fields.Integer
    }

child_medical_condition_fields = {
    'id': fields.Integer,
    'child_id': fields.Integer,
    'medical_condition_id': fields.Integer
    }

child_medication_fields = {
    'id': fields.Integer,
    'child_medication_start_date': Date,
    'child_medication_end_date': Date,
    'child_id': fields.Integer,
    'medication_id': fields.Integer,
    'dosage1': fields.Float,
    'dosage2': fields.Float,
    'dosage3': fields.Float
    }

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    #'password': fields.String
    'is_admin': fields.Boolean,
    'is_editor': fields.Boolean
}
