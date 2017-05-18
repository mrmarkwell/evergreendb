from marshallers import *
from parsers import *
from app.models import *
################ Look Up Tables ###############

class EntityData:
    def __init__(self, class_type, marshaller, create_parser, update_parser):
        self.class_type = class_type
        self.marshaller = marshaller
        self.create_parser = create_parser
        self.update_parser = update_parser

entity_data = {
    'child'                  : EntityData(Child, child_fields, child_parser, child_update_parser),
    'child_note'             : EntityData(ChildNote, child_note_fields, child_note_parser, child_note_update_parser),
    'partner'                : EntityData(Partner, partner_fields, partner_parser, partner_update_parser),
    'caregiver'              : EntityData(Caregiver, caregiver_fields, caregiver_parser, caregiver_update_parser),
    'specialist'             : EntityData(Specialist, specialist_fields, specialist_parser, specialist_update_parser),
    'specialist_type'        : EntityData(SpecialistType, specialist_type_fields, specialist_type_parser, specialist_type_update_parser),
    'milestone_type_category': EntityData(MilestoneTypeCategory, milestone_type_category_fields, milestone_type_category_parser, milestone_type_category_update_parser),
    'milestone_type'         : EntityData(MilestoneType, milestone_type_fields, milestone_type_parser, milestone_type_update_parser),
    'doctor_type'            : EntityData(DoctorType, doctor_type_fields, doctor_type_parser, doctor_type_update_parser),
    'doctor'                 : EntityData(Doctor, doctor_fields, doctor_parser, doctor_update_parser),
    'measurement_type'       : EntityData(MeasurementType, measurement_type_fields, measurement_type_parser, measurement_type_update_parser),
    'camp'                   : EntityData(Camp, camp_fields, camp_parser, camp_update_parser),
    'medical_condition'      : EntityData(MedicalCondition, medical_condition_fields, medical_condition_parser, medical_condition_update_parser),
    'medication'             : EntityData(Medication, medication_fields, medication_parser, medication_update_parser),
    'child_partner'          : EntityData(ChildPartner, child_partner_fields, child_partner_parser, child_partner_update_parser),
    'child_camp'             : EntityData(ChildCamp, child_camp_fields, child_camp_parser, child_camp_update_parser),
    'child_assessment'       : EntityData(ChildAssessment, child_assessment_fields, child_assessment_parser, child_assessment_update_parser),
    'child_caregiver'        : EntityData(ChildCaregiver, child_caregiver_fields, child_caregiver_parser, child_caregiver_update_parser),
    'child_measurement'      : EntityData(ChildMeasurement, child_measurement_fields, child_measurement_parser, child_measurement_update_parser),
    'child_milestone'        : EntityData(ChildMilestone, child_milestone_fields, child_milestone_parser, child_milestone_update_parser),
    'child_doctor_visit'     : EntityData(ChildDoctorVisit, child_doctor_visit_fields, child_doctor_visit_parser, child_doctor_visit_update_parser),
    'child_medical_condition': EntityData(ChildMedicalCondition, child_medical_condition_fields, child_medical_condition_parser, child_medical_condition_update_parser),
    'child_medication'       : EntityData(ChildMedication, child_medication_fields, child_medication_parser, child_medication_update_parser)
}

entity_names = entity_data.keys()
