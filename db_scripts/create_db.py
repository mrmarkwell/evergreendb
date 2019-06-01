# Author: Matthew Markwell
# Date: 5/2/2017
# 
# This file creates a new MySQL database.
# By default it will call the database 'testevergreendb'.
# Optionally, a database name can be passed in from the command line.
# The evergreendb tables are created in this new database.
#
# This is not production code - it is just a way to construct 
# the database for testing. The production version should probably
# use the flask mysql API and have much better error handling.

import MySQLdb as db
import sys

db_name = "testevergreendb"
if (len(sys.argv) > 1):
    db_name = sys.argv[1]


# Create the database if it doesn't exist
con = db.connect(user='aaaa', passwd='aaaa', use_unicode=True)
cur = con.cursor()
create_cmd = "CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8 COLLATE utf8_general_ci" % db_name
cur.execute(create_cmd)

con = db.connect(user='aaaa', passwd='aaaa', db=db_name, use_unicode=True)
cur = con.cursor()
           
cur.execute("""
CREATE TABLE IF NOT EXISTS Child (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
Nickname VARCHAR(255),
Sex CHAR(1),
BirthDate DATE,
ChildPhoto BLOB,
AbandonmentDate DATE,
ProgramEntryDate DATE,
ProgramDepartureDate DATE,
ProgramDepartureReason TEXT,
ChildHistory TEXT,
IsActive BOOL,
MedicalHistory TEXT,
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS Partner (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
Email VARCHAR(255),
Address VARCHAR(255),
Phone VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS Specialist (
ID CHAR(16),
AssessmentSpecialty VARCHAR(255),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS AssessmentType (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS MilestoneTypeCategory (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS MilestoneType (
ID CHAR(16),
MilestoneCategory CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
PRIMARY KEY (ID),
CONSTRAINT fk_MilestoneCategory 
FOREIGN KEY (MilestoneCategory)
REFERENCES MilestoneTypeCategory(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS DoctorType (
ID CHAR(16),
DoctorType VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS Doctor (
ID CHAR(16),
DoctorType CHAR(16),
FacilityEnglishName VARCHAR(255),
FacilityChineseName VARCHAR(255),
FacilityPinyinName VARCHAR(255),
DoctorEnglishName VARCHAR(255),
DoctorChineseName VARCHAR(255),
DoctorPinyinName VARCHAR(255),
PRIMARY KEY (ID),
CONSTRAINT fk_DoctorType 
FOREIGN KEY (DoctorType)
REFERENCES DoctorType(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS MeasurementType (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
Units VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS Caregiver (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS Camp (
ID CHAR(16),
EnglishCampName VARCHAR(255),
ChineseCampName VARCHAR(255),
PinyinCampName VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS Medication (
ID CHAR(16),
EnglishName VARCHAR(255),
ChineseName VARCHAR(255),
PinyinName VARCHAR(255),
DoseInMilligrams FLOAT,
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS MedicalCondition (
ID CHAR(16),
EnglishName VARCHAR(255),
PinyinName VARCHAR(255),
ChineseName VARCHAR(255),
PRIMARY KEY (ID)
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildPartner (
ChildID CHAR(16),
PartnerID CHAR(16),
StartDate DATE,
EndDate DATE,
Notes TEXT,
Flag BOOL,
CONSTRAINT fk_PartnerChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_PartnerID
FOREIGN KEY (PartnerID)
REFERENCES Partner(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildNote (
ChildID CHAR(16),
NoteDate DATE,
Notes TEXT,
Flag BOOL,
CONSTRAINT fk_NoteChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildCamp (
ChildID CHAR(16),
CampID CHAR(16),
CampStartDate DATE,
Notes TEXT,
CONSTRAINT fk_CampChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_CampID 
FOREIGN KEY (CampID)
REFERENCES Camp(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildAssessment (
ChildID CHAR(16),
SpecialistID CHAR(16),
AssessmentTypeID CHAR(16),
AssessmentDate DATE,
Notes TEXT,
Flag BOOL,
CONSTRAINT fk_AssessmentChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_SpecialistID 
FOREIGN KEY (SpecialistID)
REFERENCES Specialist(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_AssessmentTypeID
FOREIGN KEY (AssessmentTypeID)
REFERENCES AssessmentType(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildCaregiverHistory (
ChildID CHAR(16),
CaregiverID CHAR(16),
StartDate DATE,
EndDate DATE,
Notes TEXT,
CONSTRAINT fk_CareHistoryChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_CaregiverID
FOREIGN KEY (CaregiverID)
REFERENCES Caregiver(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildMeasurement (
ChildID CHAR(16),
MeasurementTypeID CHAR(16),
MeasurementDate DATE,
MeasurementValue FLOAT,
CONSTRAINT fk_MeasurementChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_MeasurementTypeID
FOREIGN KEY (MeasurementTypeID)
REFERENCES MeasurementType(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildMilestone (
ChildID CHAR(16),
MilestoneTypeID CHAR(16),
DateReached DATE,
CONSTRAINT fk_MilestoneChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_MilestoneTypeID
FOREIGN KEY (MilestoneTypeID)
REFERENCES MilestoneType(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildDoctorVisitHistory (
ChildID CHAR(16),
DoctorID CHAR(16),
VisitDate DATE,
Notes TEXT,
CONSTRAINT fk_DoctorHistoryChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_DoctorID
FOREIGN KEY (DoctorID)
REFERENCES Doctor(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildMedicalCondition (
ChildID CHAR(16),
MedicalConditionID CHAR(16),
CONSTRAINT fk_MecicalConditionChildID 
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_MedicalConditionID
FOREIGN KEY (MedicalConditionID)
REFERENCES MedicalCondition(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
cur.execute("""
CREATE TABLE IF NOT EXISTS ChildMedication (
ChildID CHAR(16),
MedicationID CHAR(16),
IsActive BOOL,
StartDate DATE,
EndDate DATE,
Dosage1 FLOAT,
Dosage2 FLOAT,
Dosage3 FLOAT,
CONSTRAINT fk_MedicationChildID
FOREIGN KEY (ChildID)
REFERENCES Child(ID)
ON DELETE CASCADE
ON UPDATE CASCADE,
CONSTRAINT fk_MedicationID
FOREIGN KEY (MedicationID)
REFERENCES Medication(ID)
ON DELETE CASCADE
ON UPDATE CASCADE
)
"""
)
