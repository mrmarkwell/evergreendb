from flask_restful import reqparse
from datetime import datetime

def datetype(x):
    if not x:
        return None
    return datetime.strptime(x, '%Y-%m-%d')
date_error_help = 'Date fields should be entered as: YYYY-MM-DD'

################ Parsers ####################

# A base entity parser for other parsers to derive from
base_parser = reqparse.RequestParser()

#============== FSS Parsers ================#

fss_child_parser = reqparse.RequestParser()
fss_child_parser.add_argument('child_english_name')
fss_child_parser.add_argument('child_chinese_name')
fss_child_parser.add_argument('child_pinyin_name')
fss_child_parser.add_argument('nickname')
fss_child_parser.add_argument('gender')
fss_child_parser.add_argument('birth_date', type=datetype, help=date_error_help)
fss_child_parser.add_argument('referred_by')
fss_child_parser.add_argument('status')
fss_child_parser.add_argument('primary_diagnosis')
fss_child_parser.add_argument('primary_diagnosis_note')
fss_child_parser.add_argument('secondary_diagnosis')
fss_child_parser.add_argument('secondary_diagnosis_note')
fss_child_parser.add_argument('further_diagnosis')
fss_child_parser.add_argument('reason_for_referral')
fss_child_parser.add_argument('birth_history')
fss_child_parser.add_argument('medical_history')


fss_family_member_parser = reqparse.RequestParser()
fss_family_member_parser.add_argument('child_id', type=int)
fss_family_member_parser.add_argument('relationship')
fss_family_member_parser.add_argument('family_member_name')
fss_family_member_parser.add_argument('family_member_phone')
fss_family_member_parser.add_argument('family_member_email')
fss_family_member_parser.add_argument('family_member_wechat')
fss_family_member_parser.add_argument('family_member_address')
fss_family_member_parser.add_argument('family_member_notes')
fss_family_member_parser.add_argument('family_member_is_primary', type=bool)


fss_projected_pathway_parser = reqparse.RequestParser()
fss_projected_pathway_parser.add_argument('child_id', type=int)
fss_projected_pathway_parser.add_argument('pathway_step_number')
fss_projected_pathway_parser.add_argument('pathway_short_description')
fss_projected_pathway_parser.add_argument('pathway_details')
fss_projected_pathway_parser.add_argument('pathway_completion_date', type=datetype, help=date_error_help)


fss_interaction_parser = reqparse.RequestParser()
fss_interaction_parser.add_argument('child_id', type=int)
fss_interaction_parser.add_argument('interaction_date', type=datetype, help=date_error_help)
fss_interaction_parser.add_argument('interaction_type')
fss_interaction_parser.add_argument('interaction_coordinator')
fss_interaction_parser.add_argument('people_present')
fss_interaction_parser.add_argument('is_initial_interaction', type=bool)
fss_interaction_parser.add_argument('current_concerns')
fss_interaction_parser.add_argument('dev_history')
fss_interaction_parser.add_argument('dev_since_last_visit')
fss_interaction_parser.add_argument('follow_up')
fss_interaction_parser.add_argument('interaction_notes')

fss_interaction_parser.add_argument('milk_feeding', type=bool)
fss_interaction_parser.add_argument('solid_feeding', type=bool)
fss_interaction_parser.add_argument('self_feeding', type=bool)
fss_interaction_parser.add_argument('texture_preferences')
fss_interaction_parser.add_argument('feeding_recommendations')
fss_interaction_parser.add_argument('developmental_notes')
fss_interaction_parser.add_argument('developmental_recommendations')
fss_interaction_parser.add_argument('ot_notes') 
fss_interaction_parser.add_argument('ot_recommendations')
fss_interaction_parser.add_argument('sensory_notes')
fss_interaction_parser.add_argument('sensory_recommendations')
fss_interaction_parser.add_argument('speech_notes')
fss_interaction_parser.add_argument('speech_recommendations')
fss_interaction_parser.add_argument('head_control', type=bool)
fss_interaction_parser.add_argument('rolling', type=bool)
fss_interaction_parser.add_argument('sitting', type=bool)
fss_interaction_parser.add_argument('standing', type=bool)
fss_interaction_parser.add_argument('walking', type=bool)
fss_interaction_parser.add_argument('physical_recommendations')
fss_interaction_parser.add_argument('gross_motor_notes')
fss_interaction_parser.add_argument('gross_motor_recommendations')
fss_interaction_parser.add_argument('fine_motor_notes')
fss_interaction_parser.add_argument('fine_motor_recommendations')
fss_interaction_parser.add_argument('weakness_notes')
fss_interaction_parser.add_argument('weakness_recommendations')

#============== SOAR Parsers ================#

# Parser for input date related to a child object.
child_parser = base_parser.copy()
child_parser.add_argument('child_english_name', required=True)
child_parser.add_argument('child_chinese_name')
child_parser.add_argument('child_pinyin_name')
child_parser.add_argument('nickname')
child_parser.add_argument('sex', required=True)
child_parser.add_argument('birth_date', type=datetype, help=date_error_help)
child_parser.add_argument('abandonment_date', type=datetype, help=date_error_help)
child_parser.add_argument('program_entry_date', type=datetype, help=date_error_help)
child_parser.add_argument('program_departure_date', type=datetype, help=date_error_help)
child_parser.add_argument('program_departure_reason')
child_parser.add_argument('child_history')
child_parser.add_argument('medical_history')

# When updating a child, no argument is required
# so replace arguments fields from the original child_parser.
child_update_parser = child_parser.copy()
child_update_parser.replace_argument('child_english_name', required=False)
child_update_parser.replace_argument('sex', required=False)

# child_note
child_note_parser = reqparse.RequestParser()
child_note_parser.add_argument('child_note_date', type=datetype, help=date_error_help)
child_note_parser.add_argument('child_note', required=True)
child_note_parser.add_argument('child_note_flag', type=bool)
child_note_parser.add_argument('child_id', type=int, required=True)

child_note_update_parser = child_note_parser.copy()
child_note_update_parser.replace_argument('note', required=False)
child_note_update_parser.replace_argument('child_id', type=int, required=False)
child_note_update_parser.replace_argument('child_note', required=False)

# partner
partner_parser = base_parser.copy()
partner_parser.add_argument('partner_english_name', required=True)
partner_parser.add_argument('partner_chinese_name')
partner_parser.add_argument('partner_pinyin_name')
partner_parser.add_argument('email')
partner_parser.add_argument('phone')

partner_update_parser = partner_parser.copy()
partner_update_parser.replace_argument('partner_english_name', required=False)

# caregiver
caregiver_parser = base_parser.copy()
caregiver_parser.add_argument('caregiver_english_name', required=True)
caregiver_parser.add_argument('caregiver_chinese_name')
caregiver_parser.add_argument('caregiver_pinyin_name')

caregiver_update_parser = caregiver_parser.copy()
caregiver_update_parser.replace_argument('caregiver_english_name', required=False)

# specialist

specialist_parser = base_parser.copy()
specialist_parser.add_argument('specialist_english_name', required=True)
specialist_parser.add_argument('specialist_chinese_name')
specialist_parser.add_argument('specialist_pinyin_name')
specialist_parser.add_argument('specialist_type_id', type=int, required=True)
specialist_update_parser = specialist_parser.copy()
for arg in specialist_update_parser.args:
    specialist_update_parser.replace_argument(arg, required=False)

# specialist_type

specialist_type_parser = base_parser.copy()
specialist_type_parser.add_argument('specialist_type_english_name', required=True)
specialist_type_parser.add_argument('specialist_type_chinese_name')
specialist_type_parser.add_argument('specialist_type_pinyin_name')
specialist_type_update_parser = specialist_type_parser.copy()
for arg in specialist_type_update_parser.args:
    specialist_type_update_parser.replace_argument(arg, required=False)

# milestone_type_category

milestone_type_category_parser = base_parser.copy()
milestone_type_category_parser.add_argument('milestone_type_category_english_name', required=True)
milestone_type_category_parser.add_argument('milestone_type_category_chinese_name')
milestone_type_category_parser.add_argument('milestone_type_category_pinyin_name')
milestone_type_category_update_parser = milestone_type_category_parser.copy()
for arg in milestone_type_category_update_parser.args:
    milestone_type_category_update_parser.replace_argument(arg, required=False)

# milestone_type

milestone_type_parser = base_parser.copy()
milestone_type_parser.add_argument('milestone_type_english_name', required=True)
milestone_type_parser.add_argument('milestone_type_chinese_name')
milestone_type_parser.add_argument('milestone_type_pinyin_name')
milestone_type_parser.add_argument('milestone_type_category_id', type=int, required=True)
milestone_type_update_parser = milestone_type_parser.copy()
for arg in milestone_type_update_parser.args:
    milestone_type_update_parser.replace_argument(arg, required=False)
    milestone_type_update_parser.replace_argument('milestone_type_category_id', type=int, required=False)

# doctor_type

doctor_type_parser = base_parser.copy()
doctor_type_parser.add_argument('doctor_type_english_name', required=True)
doctor_type_parser.add_argument('doctor_type_chinese_name')
doctor_type_parser.add_argument('doctor_type_pinyin_name')
doctor_type_update_parser = doctor_type_parser.copy()
for arg in doctor_type_update_parser.args:
    doctor_type_update_parser.replace_argument(arg, required=False)

# doctor

doctor_parser = reqparse.RequestParser()
doctor_parser.add_argument('doctor_english_name', required=True)
doctor_parser.add_argument('doctor_chinese_name')
doctor_parser.add_argument('doctor_pinyin_name')
doctor_parser.add_argument('facility_english_name')
doctor_parser.add_argument('facility_chinese_name')
doctor_parser.add_argument('facility_pinyin_name')
doctor_parser.add_argument('doctor_type_id', type=int, required=True)
doctor_update_parser = doctor_parser.copy()
for arg in doctor_update_parser.args:
    doctor_update_parser.replace_argument(arg, required=False)

# measurement_type

measurement_type_parser = base_parser.copy()
measurement_type_parser.add_argument('measurement_type_english_name', required=True)
measurement_type_parser.add_argument('measurement_type_chinese_name')
measurement_type_parser.add_argument('measurement_type_pinyin_name')
measurement_type_parser.add_argument('units', required=True)
measurement_type_update_parser = measurement_type_parser.copy()
for arg in measurement_type_update_parser.args:
    measurement_type_update_parser.replace_argument(arg, required=False)

# camp

camp_parser = base_parser.copy()
camp_parser.add_argument('camp_english_name', required=True)
camp_parser.add_argument('camp_chinese_name')
camp_parser.add_argument('camp_pinyin_name')
camp_update_parser = camp_parser.copy()
for arg in camp_update_parser.args:
    camp_update_parser.replace_argument(arg, required=False)

# medical_condition

medical_condition_parser = base_parser.copy()
medical_condition_parser.add_argument('medical_condition_english_name', required=True)
medical_condition_parser.add_argument('medical_condition_chinese_name')
medical_condition_parser.add_argument('medical_condition_pinyin_name')
medical_condition_update_parser = medical_condition_parser.copy()
for arg in medical_condition_update_parser.args:
    medical_condition_update_parser.replace_argument(arg, required=False)

# medication

medication_parser = base_parser.copy()
medication_parser.add_argument('medication_english_name', required=True)
medication_parser.add_argument('medication_chinese_name')
medication_parser.add_argument('medication_pinyin_name')
medication_parser.add_argument('milligram_dose', type=float, required=True)
medication_update_parser = medication_parser.copy()
for arg in medication_update_parser.args:
    medication_update_parser.replace_argument(arg, required=False)

# child_partner
child_partner_parser = reqparse.RequestParser()
child_partner_parser.add_argument('child_partner_start_date', type=datetype, help=date_error_help)
child_partner_parser.add_argument('child_partner_end_date', type=datetype, help=date_error_help)
child_partner_parser.add_argument('child_partner_note')
child_partner_parser.add_argument('child_partner_note_flag', type=bool)
child_partner_parser.add_argument('child_id', type=int, required=True)
child_partner_parser.add_argument('partner_id', type=int, required=True)

child_partner_update_parser = child_partner_parser.copy()
child_partner_update_parser.replace_argument('child_id', type=int, required=False)
child_partner_update_parser.replace_argument('partner_id', type=int, required=False)

# child_camp
child_camp_parser = reqparse.RequestParser()
child_camp_parser.add_argument('child_camp_date', required=True, type=datetype, help=date_error_help)
child_camp_parser.add_argument('child_camp_note')
child_camp_parser.add_argument('child_id', type=int, required=True)
child_camp_parser.add_argument('camp_id', type=int, required=True)

child_camp_update_parser = child_camp_parser.copy()
child_camp_update_parser.replace_argument('child_camp_date', required=False, type=datetype, help=date_error_help)
child_camp_update_parser.replace_argument('child_id', type=int, required=False)
child_camp_update_parser.replace_argument('camp_id', type=int, required=False)

# child_assessment

child_assessment_parser = reqparse.RequestParser()
child_assessment_parser.add_argument('child_assessment_date', required=True, type=datetype, help=date_error_help)
child_assessment_parser.add_argument('child_assessment_note')
child_assessment_parser.add_argument('child_id', type=int, required=True)
child_assessment_parser.add_argument('child_assessment_note_flag', type=bool)
child_assessment_parser.add_argument('specialist_id', type=int, required=True)

child_assessment_update_parser = child_assessment_parser.copy()
child_assessment_update_parser.replace_argument('child_assessment_date', required=False, type=datetype, help=date_error_help)
child_assessment_update_parser.replace_argument('child_id', type=int, required=False)
child_assessment_update_parser.replace_argument('specialist_id', type=int, required=False)

# child_caregiver

child_caregiver_parser = reqparse.RequestParser()
child_caregiver_parser.add_argument('child_caregiver_start_date', type=datetype, help=date_error_help)
child_caregiver_parser.add_argument('child_caregiver_end_date', type=datetype, help=date_error_help)
child_caregiver_parser.add_argument('child_caregiver_note')
child_caregiver_parser.add_argument('child_id', type=int, required=True)
child_caregiver_parser.add_argument('caregiver_id', type=int, required=True)

child_caregiver_update_parser = child_caregiver_parser.copy()
child_caregiver_update_parser.replace_argument('child_id', type=int, required=False)
child_caregiver_update_parser.replace_argument('caregiver_id', type=int, required=False)

# child_measurement

child_measurement_parser = reqparse.RequestParser()
child_measurement_parser.add_argument('child_measurement_date', required=True, type=datetype, help=date_error_help)
child_measurement_parser.add_argument('child_measurement_value', required=True, type=float)
child_measurement_parser.add_argument('child_measurement_comment')
child_measurement_parser.add_argument('child_id', type=int, required=True)
child_measurement_parser.add_argument('measurement_type_id', type=int, required=True)

child_measurement_update_parser = child_measurement_parser.copy()
child_measurement_update_parser.replace_argument('child_measurement_date', required=False, type=datetype, help=date_error_help)
child_measurement_update_parser.replace_argument('child_id', type=int, required=False)
child_measurement_update_parser.replace_argument('measurement_type_id', type=int, required=False)
child_measurement_update_parser.replace_argument('child_measurement_value', required=False, type=float)

# child_milestone

child_milestone_parser = reqparse.RequestParser()
child_milestone_parser.add_argument('child_milestone_date', required=True, type=datetype, help=date_error_help)
child_milestone_parser.add_argument('child_id', type=int, required=True)
child_milestone_parser.add_argument('milestone_type_id', type=int, required=True)

child_milestone_update_parser = child_milestone_parser.copy()
child_milestone_update_parser.replace_argument('child_milestone_date', required=False, type=datetype, help=date_error_help)
child_milestone_update_parser.replace_argument('child_id', type=int, required=False)
child_milestone_update_parser.replace_argument('milestone_type_id', type=int, required=False)

# child_doctor_visit

child_doctor_visit_parser = reqparse.RequestParser()
child_doctor_visit_parser.add_argument('child_doctor_visit_date', required=True, type=datetype, help=date_error_help)
child_doctor_visit_parser.add_argument('child_id', type=int, required=True)
child_doctor_visit_parser.add_argument('doctor_id', type=int, required=True)
child_doctor_visit_parser.add_argument('child_doctor_visit_note')

child_doctor_visit_update_parser = child_doctor_visit_parser.copy()
child_doctor_visit_update_parser.replace_argument('child_doctor_visit_date', required=False, type=datetype, help=date_error_help)
child_doctor_visit_update_parser.replace_argument('child_id', type=int, required=False)
child_doctor_visit_update_parser.replace_argument('doctor_id', type=int, required=False)

# child_medical_condition

child_medical_condition_parser = reqparse.RequestParser()
child_medical_condition_parser.add_argument('child_id', type=int, required=True)
child_medical_condition_parser.add_argument('medical_condition_id', type=int, required=True)

child_medical_condition_update_parser = child_medical_condition_parser.copy()
child_medical_condition_update_parser.replace_argument('child_id', type=int, required=False)
child_medical_condition_update_parser.replace_argument('medical_condition_id', type=int, required=False)

# child_medication

child_medication_parser = reqparse.RequestParser()
child_medication_parser.add_argument('child_medication_start_date', required=True, type=datetype, help=date_error_help)
child_medication_parser.add_argument('child_medication_end_date', type=datetype, help=date_error_help)
child_medication_parser.add_argument('dosage1', type=float)
child_medication_parser.add_argument('dosage2', type=float)
child_medication_parser.add_argument('dosage3', type=float)
child_medication_parser.add_argument('child_id', type=int, required=True)
child_medication_parser.add_argument('medication_id', type=int, required=True)

child_medication_update_parser = child_medication_parser.copy()
child_medication_update_parser.replace_argument('child_medication_start_date', required=False, type=datetype, help=date_error_help)
child_medication_update_parser.replace_argument('child_id', type=int, required=False)
child_medication_update_parser.replace_argument('medication_id', type=int, required=False)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True)
user_parser.add_argument('password', required=True)
user_parser.add_argument('is_admin', type=bool, required=True)
user_parser.add_argument('is_editor', type=bool, required=True)

user_update_parser = user_parser.copy()
user_update_parser.replace_argument('password', required=False)
user_update_parser.replace_argument('is_admin', type=bool, required=False)
user_update_parser.replace_argument('is_editor', type=bool, required=False)
