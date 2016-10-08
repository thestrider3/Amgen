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

def getUniversityList(conn):
    metadata = MetaData(conn)
    colleges = Table('colleges',metadata,autoload=True)
    rs = select([colleges.c.name]).execute()
    rs = [item[0] for item in rs.fetchall()]
    return rs    
    
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
    formDict=rs.fetchone()
    return dict(formDict)

def createNewUser(conn,name,passwrd):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==name)
    rs = s.execute()
    if rs.fetchone():
        return None
    conn.execute('Insert into columbiaamgen.studentData(`Username`,`Password`) Values (%s,%s)', [name,passwrd])
    formDict = {"Username":name}
    return formDict
    
def getUser(conn,username):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==username)
    rs = s.execute()
    formDict=rs.fetchone()
    return formDict


'''
def insertFirstForm(conn,userid,formDict):
=======
def insertFirstForm(conn,username,formDict):
>>>>>>> 7976302f4271f25f8d4c5bb350370076f2c2ed2d
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

def insertFirstForm(conn,formDict):
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    HowDidYouHear=""
    for sen in formDict['HowDidYouHear']:
        HowDidYouHear = HowDidYouHear+" "+ str(sen)
    i = studentData.update().where(studentData.c.Username == formDict['Username']).values(
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
    HomeState  = formDict['HomeState'],
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
    DateSpringSemesterEnds  = formDict['DateSpringSemesterEnds'],
    EthnicityOther=formDict["EthnicityOther"],
    PlaceOfBirth=formDict['PlaceOfBirth'],
    AdvancedDegreeObjectiveOther=formDict['AdvancedDegreeObjectiveOther'])
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
