# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:28:00 2016

@author: shivani
"""

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from user import *
DATABASEURI = "mysql+mysqlconnector://aheicklen:mass67@mysql.columbiasurf.dreamhosters.com:3306/columbiaamgen" 
engine = create_engine(DATABASEURI)

def createDatabaseConnection():
    try:
        conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        conn = None
    return conn,engine
    
def checkUser(conn,name,passwrd):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(and_(user_info.c.Username==name , user_info.c.Password==passwrd))
    rs = s.execute()
    a=rs.fetchone()
    if a:
        u = User(a["Username"],a["Password"])
        return u

def createNewUser(conn,name,passwrd):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==name)
    rs = s.execute()
    if rs.fetchone():
        return null
    conn.execute('Insert into columbiaamgen.studentData(`Username`,`Password`) Values (%s,%s)', [name,passwrd])
    u = User(name,passwrd)
    return u
    
def getUser(conn,username):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==username)
    rs = s.execute()
    a=rs.fetchone()
    u = User(a["Username"],a["Password"])
    return u
'''
def insertFirstForm(conn,userid,formDict):
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
  '''