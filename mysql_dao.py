# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:28:00 2016

@author: shivani
"""

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from user import *

from UserType import UserType
DATABASEURI = "mysql+mysqlconnector://aheicklen:mass67@mysql.columbiasurf.dreamhosters.com:3306/columbiaamgen" 
engine = create_engine(DATABASEURI)

def getUniversityList(conn):
    metadata = MetaData(conn)
    colleges = Table('colleges',metadata,autoload=True)
    rs = select([colleges.c.name]).execute()
    rs = [item[0] for item in rs.fetchall()]
    return rs 

def getMentorsList(conn):
    metadata = MetaData(conn)
    mentors = Table('Mentors',metadata,autoload=True)
    rs = select([mentors.c.Name]).execute()
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
    formDict=dict(formDict)
    
    if formDict:
        courses = Table('Courses', metadata, autoload=True)
        s= courses.select(courses.c.UserId==name)
        rs=s.execute()
        i=0
        for row in rs:
            formDict['stitle'+''+str(i)] = row['Title']
            formDict['scredits'+''+str(i)] = row['Credits']
            formDict['sgrade'+''+str(i)] = row['Grade']
            i=i+1
    return formDict

def createNewUser(conn,name,passwrd,status):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==name)
    rs = s.execute()
    if rs.fetchone():
        return None
    conn.execute('Insert into columbiaamgen.studentData(`Username`,`Password`,`ApplicationStatus`) Values (%s,%s,%s)', [name,passwrd,status])
    formDict = {"Username":name,"ApplicationStatus":status}
    return formDict
    
def getUser(conn,username):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==username)
    rs = s.execute()
    formDict=rs.fetchone()
    formDict=dict(formDict)
    
    if formDict:
        courses = Table('Courses', metadata, autoload=True)
        s= courses.select(courses.c.UserId==username)
        rs=s.execute()
        i=0
        for row in rs:
            formDict['stitle'+''+str(i)] = row['Title']
            formDict['scredits'+''+str(i)] = row['Credits']
            formDict['sgrade'+''+str(i)] = row['Grade']
            i=i+1
    return formDict

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

def insertSecondForm(conn,formDict):
    print()
    print(formDict)
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    i = studentData.update().where(studentData.c.Username == formDict['Username']).values(
    ScienceExperience = formDict['ScienceExperience'],  
    CareerPlans = formDict['CareerPlans'],  
    AspirationNext20Yrs = formDict['AspirationNext20Yrs'],
    ApplicationStatus = formDict['ApplicationStatus'],  
    Mentor1 = formDict['Mentor1'],  
    Mentor2 = formDict['Mentor2'],  
    Mentor3 = formDict['Mentor3'],  
    Mentor4 = formDict['Mentor4'], 
    Mentor5 = formDict['Mentor5'])  
    #Transcript = formDict['Transcript'],  
    #IsApplicationSubmitted = formDict['IsApplicationSubmitted'])
    conn.execute(i)
    
    Courses = Table('Courses',metadata, autoload=True)
    for i in range(0,26):
        if 'stitle'+''+str(i) in formDict:
            print('formDict not none')
            query = Courses.select(and_(Courses.c.UserId==formDict['Username'],Courses.c.Title==formDict['stitle'+''+str(i)]))
            rs = query.execute()
            if rs.fetchone():
                query = Courses.delete().where(and_(Courses.c.UserId==formDict['Username'],Courses.c.Title==formDict['stitle'+''+str(i)]))
                conn.execute(query)
            query = Courses.insert().values(
            UserId = formDict['Username'],
            Title = formDict['stitle'+''+str(i)],  
            Credits = formDict['scredits'+''+str(i)],  
            Grade = formDict['sgrade'+''+str(i)])
            conn.execute(query)
        else:
            break

def insertThirdForm(conn, formDict):
    metadata = MetaData(conn)
    References = Table('References',metadata, autoload=True)
    for i in range(0,2):
        i = References.insert().values(
        UserId = formDict['Username'],
        Name = formDict['RefName'+str(i)],  
        Email = formDict['RefEmail'+str(i)])
        conn.execute(i)

def insertReviewWaiver(conn, formDict):
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    i = studentData.update().where(studentData.c.Username == formDict['Username']).values(
    ReviewWaiver = formDict['ReviewWaiver'])
    conn.execute(i)

def deleteThirdForm(conn, formDict):
    MetaData = MetaData(conn)
    References = Table('References',metadata, autoload=True)
    for i in range(0,2):
        i = References.delete().where(
        UserId == formDict['Username'])
        conn.execute(i)

def getStudentList(conn):
    metadata = MetaData(conn)
    studentData = Table('studentData', metadata, autoload=True)
    s= select([studentData.c.Username,studentData.c.FirstName,studentData.c.LastName]).where(studentData.c.UserType == UserType.Student.name)
    rs = s.execute().fetchall()
    #print(rs)
    '''
    studentDict = dict()
    for row in rs:
        studentDict['UserName'] = row[0]
        studentDict['FirstName'] = row[1]
        studentDict['LastName'] = row[2]
    print(studentDict)
    '''
    return rs
      

