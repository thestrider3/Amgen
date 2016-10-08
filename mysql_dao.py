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

def insertFirstForm(conn,username,formDict):
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    HowDidYouHear=""
    for sen in formDict['HowDidYouHear']:
        HowDidYouHear = HowDidYouHear+" "+ str(sen)
    i = studentData.update().where(studentData.c.Username == username).values(
    FirstName = formDict['FirstName'],
    LastName  = formDict['LastName'],
    DOB = formDict['DOB'],
    Email = formDict['Email'], 
    AlternativeEmail  = formDict['AlternativeEmail'],
    Phone  = formDict['Phone'],
    PermStreetAdr1  = formDict['PermStreetAdr1'],
    PermStreetAdr2  = formDict['PermStreetAdr2'],
    PermanentCity  = formDict['PermanentCity'],
    PermanentState  = formDict['PermanentState'],
    PermanentZipCode  = formDict['PermanentZipCode'],
    CampusAdr1  = formDict['CampusAdr1'],
    CampusAdr2  = formDict['CampusAdr2'],
    CampusCity  = formDict['CampusCity'],
    CampusState  = formDict['CampusState'],
    CampusZipCode  = formDict['CampusZipCode'],
    HomeCity  = formDict['HomeCity'],
    HomeState  = formDict['UserId'],
    Gender  = formDict['Gender'],
    Ethnicity  = formDict['Ethnicity'],
    CitizenshipStatus  = formDict['CitizenshipStatus'],
    MotherDegree  = formDict['MotherDegree'],
    FatherDegree  = formDict['FatherDegree'],
    ClassCompletedSpring  = formDict['ClassCompletedSpring'],
    GraduationMonth  = formDict['GraduationMonth'],
    GraduationYear  = formDict['GraduationYear'],
    CumulativeGPA  = formDict['CumulativeGPA'],
    AdvancedDegreeObjective  = formDict['AdvancedDegreeObjective'],
    IsUndergraduateResearchProgramOffered  = formDict['IsUndergraduateResearchProgramOffered'],
    HowDidYouHear  = HowDidYouHear,
    HowDidYouHearUniversityName = formDict['HowDidYouHearUniversityName'],
    HowDidYouHearConferenceName = formDict['HowDidYouHearConferenceName'],
    HowDidYouHearOtherUniversityName = formDict['HowDidYouHearOtherUniversityName'],
    HowDidYouHearOther = formDict['HowDidYouHearOther'],
    AnyOtherAmgenScholarsSite  = formDict['AnyOtherAmgenScholarsSite'],
    YesOtherAmgenScholarsSite  = formDict['YesOtherAmgenScholarsSite'],
    PastAmgenScholarParticipation  = formDict['PastAmgenScholarParticipation'],
    OriginalResearchPerformed  = formDict['OriginalResearchPerformed'],
    CanArriveAtColumbiaMemorialDay  = formDict['CanArriveAtColumbiaMemorialDay'],
    ArriveAtColumbiaComments  = formDict['ArriveAtColumbiaComments'],
    CurrentlyAttendingUniversity  = formDict['CurrentlyAttendingUniversity'],
    Major  = formDict['Major'],
    DateSpringSemesterEnds  = formDict['DateSpringSemesterEnds'])
    conn.execute(i)

def getFirstFormData(conn,Username):
    metadata = MetaData(conn)
    studentData = Table('studentData', metadata, autoload=True)
    s= studentData.select(studentData.c.Username==Username)
    rs = s.execute()
    formDict = rs.fetchone()
    return formDict

def insertSecondForm(conn,username,formDict):
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    i = studentData.update().where(studentData.c.Username == username).values(
    ScienceExperience = formDict['ScienceExperience'],  
    CareerPlans = formDict['CareerPlans'],  
    AspirationNext20Yrs = formDict['AspirationNext20Yrs'],  
    Mentor1 = formDict['Mentor1'],  
    Mentor2 = formDict['Mentor2'],  
    Mentor3 = formDict['Mentor3'],  
    Mentor4 = formDict['Mentor4'], 
    Mentor5 = formDict['Mentor5'],  
    #Transcript = formDict['Transcript'],  
    IsApplicationSubmitted = formDict['IsApplicationSubmitted'])
    conn.execute(i)

def insertStudentCourse(conn, username, formDict, title, grade, credit):
    metadata = MetaData(conn)
    Courses = Table('Courses',metadata, autoload=True)
    i = Courses.insert().values(
    Username = username,
    Title = formDict[title],  
    Credits = formDict[credit],  
    Grade = formDict[grade])
    conn.execute(i)