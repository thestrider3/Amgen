# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:28:00 2016

@author: shivani
"""

from sqlalchemy import *
from sqlalchemy.pool import NullPool
from user import *
import string
import random
from enums import ApplicationStatus, UserType, ReferenceStatus

DATABASEURI = "mysql+mysqlconnector://amgen:744BmuDD@amgen.cyo9vivgubeb.us-west-2.rds.amazonaws.com:3306/amgen" 
engine = create_engine(DATABASEURI)

def idGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getUniversityList(conn):
    metadata = MetaData(conn)
    colleges = Table('Colleges',metadata,autoload=True)
    rs = select([colleges.c.Name]).execute()
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
    LoginData = Table('LoginData',metadata, autoload=True)
    l= LoginData.select(and_(LoginData.c.Username==name , LoginData.c.Password==passwrd))
    rs = l.execute()
    formDict=rs.fetchone()
    
    if formDict:
        formDict=dict(formDict)
        if formDict['UserType'] == UserType['Student']:
            user_info = Table('studentData', metadata, autoload=True)
            s= user_info.select(and_(user_info.c.Username==name , user_info.c.Password==passwrd))
            rs=s.execute()
            formDict=rs.fetchone()
            formDict=dict(formDict)
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

def createNewUser(conn,name,passwrd,status,userType):
    metadata = MetaData(conn)
    LoginData = Table('LoginData',metadata, autoload=True)
    l= LoginData.select( LoginData.c.Username==name )
    
    rs =l.execute()
    if rs.fetchone():
        return None
    else:
        conn.execute('Insert into amgen.LoginData(`Username`,`Password`,`Status`,`UserType`) Values (%s,%s,%s,%s)', [name,passwrd,status,userType])
        if userType==UserType['Student']:
            conn.execute('Insert into amgen.studentData(`Username`,`Password`,`ApplicationStatus`) Values (%s,%s,%s)', [name,passwrd,status])
    formDict = checkUser(conn,name,passwrd)
    return formDict
    
def getUser(conn,username):
    metadata = MetaData(conn)
    user_info = Table('studentData', metadata, autoload=True)
    s= user_info.select(user_info.c.Username==username)
    rs = s.execute()
    formDict=rs.fetchone()
    if formDict:
        formDict=dict(formDict)
    else:
        formDict=dict()
    
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
   
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    i = studentData.update().where(studentData.c.Username == formDict['Username']).values(
    ScienceExperience = formDict['ScienceExperience'],  
    CareerPlans = formDict['CareerPlans'],
    ApplicationStatus = formDict['ApplicationStatus'],  
    Mentor1 = formDict['Mentor1'],  
    Mentor2 = formDict['Mentor2'],  
    Mentor3 = formDict['Mentor3'],  
    Mentor4 = formDict['Mentor4'], 
    Mentor5 = formDict['Mentor5'],
    Transcript = formDict['Transcript'], 
    Mentor6 = formDict['Mentor6'],
    Mentor7 = formDict['Mentor7'],
    Mentor8 = formDict['Mentor8'])
    #Transcript = formDict['Transcript'],  
    #IsApplicationSubmitted = formDict['IsApplicationSubmitted'])      
    conn.execute(i)
    
    Courses = Table('Courses',metadata, autoload=True)
    for i in range(0,26):
        if 'stitle'+''+str(i) in formDict:
            
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

def reflectReferalSubmitted(conn,formDict):
    i=0
    metadata = MetaData(conn)
    References = Table('References', metadata, autoload=True)
    studentData = Table('studentData', metadata, autoload=True)
    students=[]
    while 1:
        if 'Referal'+str(i) not in formDict:
            break
        else:
            query = select([References.c.Status]).where(and_(References.c.Username == formDict['Referal'+str(i)],References.c.Email==formDict['Username']))
            rs = query.execute()
            a=rs.fetchone
            print('This is it')
            status = rs.fetchone()
            print type(status[0])
            print status[0] == 'ReferenceRequired'
            if status[0] == 'ReferenceRequired':
                students.append(formDict['Referal'+str(i)])
                query = References.update().where(and_(References.c.Username == formDict['Referal'+str(i)],References.c.Email==formDict['Username'])).values(Status=ReferenceStatus['ReferenceSubmitted'],ReferalFilePath=formDict['ReferalPath'+str(i)])
                query.execute()
            i=i+1
    
    query = studentData.update().where(and_(studentData.c.Username.in_(students),studentData.c.ApplicationStatus==ApplicationStatus['ReferencesRequired1'])).values(ApplicationStatus=ApplicationStatus['UnderReview'])
    query.execute()    

    query = studentData.update().where(and_(studentData.c.Username.in_(students),studentData.c.ApplicationStatus==ApplicationStatus['ReferencesRequired2'])).values(ApplicationStatus=ApplicationStatus['ReferencesRequired1'])
    query.execute()    

    
def getStudentsByProf(conn, username):
    """
    """

    metadata = MetaData(conn)
    References = Table('References', metadata, autoload=True)
    studentData = Table('studentData', metadata, autoload=True)

    students = [x[0] for x in select([References.c.Username]).where(References.c.Email == username).execute().fetchall()]

    query = select([studentData.c.Username,studentData.c.FirstName,studentData.c.LastName], studentData.c.Username.in_(students))

    result = query.execute().fetchall()    
    return result

def insertThirdForm(conn, formDict):
    metadata = MetaData(conn)
    newRefs=[]
    References = Table('References',metadata, autoload=True)
    StudentData = Table('studentData',metadata, autoload=True)
    curRef = References.select(References.c.Username==formDict['Username'])
    curRef = curRef.execute().fetchall();
    ins = [False,False]
    for ref in curRef:
        foundRef = False
        for i in range(1,3):
            if formDict['RefEmail'+str(i)] == ref['Email']:
                ins[i-1] = True
                foundRef=True
                References.update().where(and_(References.c.Username==formDict['Username'], References.c.Email==formDict['RefEmail'+str(i)])).values(Name = formDict['RefName'+str(i)]).execute()
        if not foundRef:
            References.delete().where(and_(References.c.Username==formDict['Username'], References.c.Email==formDict['RefEmail'+str(i)])).execute()
            
    for i in range(1,3):
        if ins[i-1] == False and formDict['RefName'+str(i)].strip() and formDict['RefEmail'+str(i)].strip():
            password=idGenerator()
            References.insert().values(Username = formDict['Username'],Name = formDict['RefName'+str(i)],Email = formDict['RefEmail'+str(i)],Status=ReferenceStatus['ReferenceRequired']).execute()
            createNewUser(conn,formDict['RefEmail'+str(i)],password,ApplicationStatus['PlaceholderAppStatus'],UserType['Referal'])
            newRefs.append((formDict['RefEmail'+str(i)],formDict['RefName'+str(i)],password))
    return newRefs

def insertReviewWaiver(conn, formDict):
    metadata = MetaData(conn)
    studentData = Table('studentData',metadata, autoload=True)
    i = studentData.update().where(studentData.c.Username == formDict['Username']).values(
    ReviewWaiver = formDict['ReviewWaiver'])
    conn.execute(i)

def deleteThirdForm(conn, formDict):
    metadata = MetaData(conn)
    References = Table('References',metadata, autoload=True)
    delete = References.select().where(
    References.c.Username == formDict['Username'])
    conn.execute(delete)
    studentData = Table('studentData', metadata, autoload=True)
    s = studentData.update().where(studentData.c.Username==formDict['Username']).values(
    ReviewWaiver = None)
    rs = s.execute()
    
    
def getReferences(conn, formDict):
    metadata = MetaData(conn)
    References = Table('References', metadata, autoload=True)
    studentData = Table('studentData', metadata, autoload=True)
    s= References.select(References.c.Username==formDict['Username'])
    rs = s.execute()
    referencesDict=rs.fetchall()
    ReferencesDict = dict()
    i = 1
    if referencesDict:
        for row in referencesDict:
            ReferencesDict['REFERENCE_'+str(i)] = row[1]
            ReferencesDict['ref'+str(i)+'email'] = row[2]
            ReferencesDict['ref'+str(i)+'status']=row[3]
            i = i + 1            
        sel = select([studentData.c.ReviewWaiver]).where(studentData.c.Username == formDict['Username'])
        ReferencesDict['ReviewWaiver'] = sel.execute().fetchone()[0]
    
        
        
    ReferencesDict=dict(ReferencesDict)
    return ReferencesDict

def getStudentList(conn):
    metadata = MetaData(conn)
    studentData = Table('studentData', metadata, autoload=True)
    s= select([studentData.c.Username,studentData.c.FirstName,studentData.c.LastName]).where(studentData.c.UserType == UserType['Student'])
    rs = s.execute().fetchall()
    return rs
    
def getTranscript(conn, username):
    metadata = MetaData(conn)
    studentData = Table('studentData', metadata, autoload=True)
    s = select([studentData.c.Transcript]).where(studentData.c.Username == username)
    filename = s.execute().fetchone()
    print(filename)
    return filename
    
def getReferralPath(conn, username):
    metadata = MetaData(conn)
    References = Table('References', metadata, autoload=True)
    s = select([References.c.ReferalFilePath]).where(References.c.Username == username)
    fs = s.execute().fetchall()
    filename=[item[0] for item in fs]
    #print(filename)
    return filename
      

