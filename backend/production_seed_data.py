# -*- coding: utf-8 -*-

#Initial admin user
# Not needed since an admin user is set up by flask-admin.
# Default is username: admin, password: admin
users = [
    (u"administrator", u"evergreen", True, True)
]

# FSS Data
medical_conditions = [
    u"CP",
    u"Autism",
    u"Intellectual Disability",
    u"ADHD",
    u"Lennox-Gastaut",
    u"Angelman Syndrome",
    u"PKU",
    u"Cleft Lip / Cleft Palate",
    u"Hepatitis B",
    u"Heart Defect",
    u"Intestinal Malrotation",
    u"Congenital Heart Defect",
    u"Spina Bifida",
    u"Down Syndrome",
    u"Physical Abnormality",
    u"Seizures",
    u"Umbilical Hernia / Gastroschisis"]

interaction_types = [
    u'Consultation SOAR Village',
    u'Consultation FSS Centre',
    u'Home visit',
    u'Phone call',
    u'E-Mail',
    u'WeChat',
    u'To Do'
]

interaction_coordinators = [
    u'Tabatha Broxholme',
    u'Hou Aiping'
]

# SOAR DATA
medications = [
    (u"Carbamazepine", u"卡马西平", 100),
    (u"Lamotrigine", u"拉莫三嗪", 50),
    (u"Phenobarbital", u"苯巴比妥", 30),
    (u"Topiramate", u"妥泰", 25),
    (u"Valproate", u"丙戊酸钠", 200),
    (u"Haloperidol", u"氟哌啶醇", 2),
    (u"Quetiapine", u"富马酸喹硫平", 100),
    (u"Risperidone", u"利培酮", 1)]

measurements = [
    (u"weight", u"kg"),
    (u"height", u"cm"),
    (u"MUAC", u"cm"),
    (u"Head Circumference", u"cm")]

doctor_types = [
    u"Paediatrician",
    u"Neurologist",
    u"Dentist",
    u"OT",
    u"PT",
    u"Ophthalmologist",
    u"EG Doctor"]

milestone_type_categories = [
    u"Communication Milestones",
    u"Physical Milestones",
    u"Life Skills"]

# Since milestone type categories are seeded in the order above,
# the second element of the below tuples is the id of the category.
milestone_types = [
    (u"Vocalizes", 1),
    (u"Responds to name", 1),
    (u"Says 2-3 words", 1),
    (u"Says several words", 1),
    (u"Says sentences containing subject & verb", 1),
    (u"Converses in sentences", 1),
    (u"Can count", 1),
    (u"Reached", 2),
    (u"Date", 2),
    (u"Sits alone", 2),
    (u"Crawls", 2),
    (u"Stands alone", 2),
    (u"Walks with assistance", 2),
    (u"Walks alone", 2),
    (u"Reached", 3),
    (u"Date", 3),
    (u"Uses simple gestures (i.e. bye-bye, shakes head)", 3),
    (u"Drinks from a cup", 3),
    (u"Eats with a spoon", 3),
    (u"Toilet trained", 3),
    (u"Scribbles", 3),
    (u"Copies shapes", 3)]

specialist_types = [
    u"OT",
    u"PT",
    u"SLP",
    u"PSY"]

camps = [
    u"Bring me Hope",
    u"Bridge of Hope",
    u"Joy in the Journey"]