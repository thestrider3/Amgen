# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:28:00 2016

@author: shivani
"""

from sqlalchemy import *
from sqlalchemy.pool import NullPool
DATABASEURI = "mysql+mysqlconnector://aheicklen:mass67@mysql.columbiasurf.dreamhosters.com:3306/columbiaamgen" 
engine = create_engine(DATABASEURI)

def createDatabaseConnection():
    try:
        conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        conn = None
    return conn
    
def createNewUser(conn,name,passwrd,userid):
    metadata = MetaData(conn)
    user_info = Table('userInfo', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==name)
    rs = s.execute()
    if rs.fetchone():
        return "Error"
    conn.execute('INSERT INTO userInfo VALUES (%s, %s, %s)', [name,passwrd,userid])
    
def getUser(conn,userid):
    metadata = MetaData(conn)
    user_info = Table('userInfo', metadata, autoload=True)
    s= user_info.select(user_info.c.Id==userid)
    rs = s.execute()
    a=rs.fetchone()
    u = User(rs["Username"],rs["Password"],rs["Id"],True)
    return u

def insertFirstForm(conn,userid,formDict)
    metadata = MetaData(conn)
    studentFormData = Table('studentFormData',metadata, autoload=True)
    i = studentFormData.merge(studentFormData.c.UserId = formDict['UserId'],
    studentFormData.c.FirstName = formDict['FirstName'],
    studentFormData.c.LastName  = formDict['LastName'],
    studentFormData.c.DOB = formDict['DOB'],
    studentFormData.c.Email = formDict['Email'], 
    studentFormData.c.AlternativeEmail  = formDict['AlternativeEmail'],
    studentFormData.c.Phone  = formDict['Phone'],
    studentFormData.c.PermStreetAdr1  = formDict['PermStreetAdr1'],
    studentFormData.c.PermStreetAdr2  = formDict['PermStreetAdr2'],
    studentFormData.c.PermanentCity  = formDict['PermanentCity'],
    studentFormData.c.PermanentState  = formDict['PermanentState'],
    studentFormData.c.PermanentZipCode  = formDict['PermanentZipCode'],
    studentFormData.c.CampusAdr1  = formDict['CampusAdr1'],
    studentFormData.c.CampusAdr2  = formDict['CampusAdr2'],
    studentFormData.c.CampusCity  = formDict['CampusCity'],
    studentFormData.c.CampusState  = formDict['CampusState'],
    studentFormData.c.CampusZipCode  = formDict['CampusZipCode'],
    studentFormData.c.HomeCity  = formDict['HomeCity'],
    studentFormData.c.HomeState  = formDict['UserId'],
    studentFormData.c.Gender  = formDict['Gender'],
    studentFormData.c.Ethnicity  = formDict['Ethnicity'],
    studentFormData.c.CitizenshipStatus  = formDict['CitizenshipStatus'],
    studentFormData.c.MotherDegree  = formDict['MotherDegree'],
    studentFormData.c.FatherDegree  = formDict['FatherDegree'],
    studentFormData.c.ClassCompletedSpring  = formDict['ClassCompletedSpring'],
    studentFormData.c.GraduationMonth  = formDict['GraduationMonth'],
    studentFormData.c.GraduationYear  = formDict['GraduationYear'],
    studentFormData.c.CumulativeGPA  = formDict['CumulativeGPA'],
    studentFormData.c.AdvancedDegreeObjective  = formDict['AdvancedDegreeObjective'],
    studentFormData.c.IsUndergraduateResearchProgramOffered  = formDict['IsUndergraduateResearchProgramOffered'],
    studentFormData.c.HowDidYouHear  = formDict['HowDidYouHear'],
    studentFormData.c.AnyOtherAmgenScholarsSite  = formDict['AnyOtherAmgenScholarsSite'],
    studentFormData.c.YesOtherAmgenScholarsSite  = formDict['YesOtherAmgenScholarsSite'],
    studentFormData.c.PastAmgenScholarParticipation  = formDict['PastAmgenScholarParticipation'],
    studentFormData.c.OriginalResearchPerformed  = formDict['OriginalResearchPerformed'],
    studentFormData.c.CanArriveAtColumbiaMemorialDay  = formDict['CanArriveAtColumbiaMemorialDay'],
    studentFormData.c.ArriveAtColumbiaComments  = formDict['ArriveAtColumbiaComments'],
    studentFormData.c.CurrentlyAttendingUniversity  = formDict['CurrentlyAttendingUniversity'],
    studentFormData.c.Major  = formDict['Major'],
    studentFormData.c.DateSpringSemesterEnds  = formDict['DateSpringSemesterEnds'])
  