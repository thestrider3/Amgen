#!/usr/bin/env python2.7

import os, uuid, json, flask, mysql_dao, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, request, flash, render_template, session, abort, g, redirect, Response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from user import *
from applicationStatus import ApplicationStatus
from UserType import UserType
import json

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__)


@app.before_request
def before_request():
    global dbcon,engine,dbSession
    dbcon,engine = mysql_dao.createDatabaseConnection()
    Session = sessionmaker(bind=engine)
    dbSession = Session()

@app.teardown_request
def teardown_request(exception):
  global dbcon
  try:
    dbcon.close()
  except Exception as e:
    pass

@app.route('/')
def main():
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        universityList = mysql_dao.getUniversityList(dbcon)
        return render_template('first.html',formDict=session['user'],universityList=universityList)
    

@app.route('/checkUsername', methods=['POST'])
def checkUsername():
  print("inside checkUsername")
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])
  
  formDict=mysql_dao.checkUser(dbcon,name,passwrd)

  #print(formDict)
  #print(UserType.Student)
  if formDict['UserType'] == UserType.Student and formDict['ApplicationStatus'] == ApplicationStatus.IncompleteApplication:
      session['logged_in'] = True
      session['user'] = formDict
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('first.html',formDict=formDict,universityList=universityList)

  elif formDict['UserType'] == UserType.Student.name and formDict['ApplicationStatus'] == ApplicationStatus.ReferencesRequired.name:
      session['logged_in'] = True
      session['user'] = formDict
      ReferencesDict = dict()
      ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
      #print(ReferencesDict)
      return render_template('third.html', ReferencesDict = ReferencesDict)  
  elif formDict['UserType'] == UserType.Student.name and formDict['ApplicationStatus'] == ApplicationStatus.UnderReview.name:
      session['logged_in'] = True
      session['user'] = formDict
      return render_template('underReview.html')
  elif formDict['UserType'] == UserType.Admin.name:
      #print("admin logging in")

      session['logged_in'] = True
      studentList = mysql_dao.getStudentList(dbcon)
      return render_template('studentList.html',studentList=studentList)
      
  else:  
      flash('Wrong username or wrong password!')

  
@app.route('/addUsername', methods=['POST'])
def addUser():
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])

  user = mysql_dao.createNewUser(dbcon,name,passwrd,ApplicationStatus.IncompleteApplication)
  
  if user:
      session['logged_in'] = True
      session['user'] = user
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('first.html',formDict=dict(),universityList=universityList)
  else:
       flash("Username already exists. Please try again.")
      
      
@app.route('/submitFirstForm', methods=['POST'])
def addFirstForm():
    l=list()
    formDict=session['user']
    
    formDict['FirstName'] = str(request.form.get('FNAME'))
    formDict['LastName'] = str(request.form.get('LNAME'))
    formDict['DOB'] = str(request.form.get('DATEOFBIRTH'))
    formDict['Email'] = str(request.form.get('EMAIL'))
    formDict['AlternativeEmail'] = str(request.form.get('ALTERNATIVE_EMAIL'))
    formDict['Phone'] = str(request.form.get('PERMANENT_PHONE'))
    formDict['PermStreetAdr1'] = str(request.form.get('PERMANENT_ADDRESS1'))
    formDict['PermStreetAdr2'] = str(request.form.get('PERMANENT_ADDRESS2'))
    formDict['PermanentCity'] = str(request.form.get('PERMANENT_CITY'))
    formDict['PermanentState'] = str(request.form.get('PERMANENT_STATE'))
    formDict['PermanentZipCode'] = str(request.form.get('PERMANENT_ZIP'))
    formDict['CampusAdr1'] = str(request.form.get('SCHOOL_ADDRESS1'))
    formDict['CampusAdr2'] = str(request.form.get('SCHOOL_ADDRESS2'))
    formDict['CampusCity'] = str(request.form.get('CAMPUS_CITY'))
    formDict['CampusState'] = str(request.form.get('CAMPUS_STATE'))
    formDict['CampusZipCode'] = str(request.form.get('CAMPUS_ZIP'))
    formDict['HomeCity'] = str(request.form.get('HOMECITY'))
    formDict['HomeState'] = str(request.form.get('HOMESTATE'))
    formDict['Gender'] = str(request.form.get('GENDER'))      
    formDict['Ethnicity'] = str(request.form.get('ethinicity')) 
    if(formDict['Ethnicity']=='Other'):
      formDict["EthnicityOther"] = str(request.form.get('ethnicityother'))
    else:
      formDict["EthnicityOther"] = ""
    formDict['CitizenshipStatus'] = str(request.form.get('CITIZENSHIP'))
    if(formDict['CitizenshipStatus']=='resident'):
        formDict['PlaceOfBirth']=str(request.form.get('PLACEOFBIRTH'))
    formDict['MotherDegree'] = str(request.form.get('MOTHERDEGREE'))
    formDict['FatherDegree'] = str(request.form.get('FATHERDEGREE'))
    formDict['ClassCompletedSpring'] = str(request.form.get('CLASSCOMPLETE'))
    formDict['GraduationMonth'] = str(request.form.get('GRADUATION_DATE'))
    formDict['GraduationYear'] = str(request.form.get('BACHELORYEAR'))
    formDict['CumulativeGPA'] = str(request.form.get('CUMULATIVEGPA'))
    formDict['AdvancedDegreeObjective'] = str(request.form.get('ADVANCEDDEGREE'))
    if(formDict['AdvancedDegreeObjective']=='Other'):
        formDict['AdvancedDegreeObjectiveOther'] = str(request.form.get('ADVANCEDDEGREEOTHER'))
    formDict['IsUndergraduateResearchProgramOffered'] = str(request.form.get('RESEARCHOFFER'))
      
    if request.form.get('AMGENSITE'):
        l.append("Amgen National Website") 
    if request.form.get('UNIVERSITYSITE'):
        l.append("University website, University name")
        formDict['HowDidYouHearUniversityName'] = str(request.form.get('UNIVERSITYSITENAME'))
    else:
        formDict['HowDidYouHearUniversityName'] = ""
    if request.form.get('EMAILANNOUNCEMENT'):
        l.append("E-mail Announcement")
    if request.form.get('POSTER'):
        l.append("Poster")
    if request.form.get('CONFERENCE'):
        l.append("Conference, Conference Name")
        formDict['HowDidYouHearConferenceName'] = str(request.form.get('CONFERENCENAME'))
    else:
        formDict['HowDidYouHearConferenceName'] = ""
    if request.form.get('ACADEMICADVISOR'):
        l.append("Academic Advisor")
    if request.form.get('INTERNETSEARCH'):
        l.append("Internet Search")
    if request.form.get('HOMEUNIVERSITY'):
        l.append("Faculty/Staff from home university") 
    if request.form.get('OTHERUNIVERSITY'):
        l.append("Faculty/Staff from home university")
        formDict['HowDidYouHearOtherUniversityName'] = str(request.form.get('OTHERUNIVERSITYNAME'))
    else:
        formDict['HowDidYouHearOtherUniversityName'] = ""
    if request.form.get('AMGENOTHER'):
        l.append("Other")
        formDict['HowDidYouHearOther'] = str(request.form.get('AMGENOTHERNAME'))
    else:
        formDict['HowDidYouHearOther'] = ""
    formDict['HowDidYouHear'] = l
    
    formDict['AnyOtherAmgenScholarsSite'] = str(request.form.get('APPLYINGOTHER'))
    formDict['YesOtherAmgenScholarsSite'] = str(request.form.get('APPLYINGOTHERSPECIFY'))
    formDict['PastAmgenScholarParticipation'] = str(request.form.get('PARTICIPATED'))
    formDict['OriginalResearchPerformed'] = str(request.form.get('UG_RESEARCH'))
    formDict['CanArriveAtColumbiaMemorialDay'] = str(request.form.get('ARRIVEONFIRSTDAY'))
    formDict['ArriveAtColumbiaComments'] = str(request.form.get('ARRIVEONFIRSTDAYX'))
    formDict['CurrentlyAttendingUniversity'] = str(request.form.get('university'))
    formDict['Major'] = str(request.form.get('MAJOR'))
    formDict['DateSpringSemesterEnds'] = str(request.form.get('SEMESTER_END'))
    mysql_dao.insertFirstForm(dbcon,formDict)
    session['user'] = formDict
      
    if request.form['submitButton'] == 'Next': 
        mentorsList = mysql_dao.getMentorsList(dbcon)
        return flask.render_template('second.html',formDict=formDict,mentorsList=mentorsList)
    elif request.form['submitButton'] == 'Save':
        universityList = mysql_dao.getUniversityList(dbcon)
        return render_template('first.html',formDict=formDict,universityList=universityList)
    elif request.form['submitButton'] == 'Logout':
        session['logged_in']=False
        session.pop('user')
        return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print(session)
        session['logged_in'] = True
        formDict = session['user']
        formDict['ScienceExperience'] = str(request.form.get('EXPERIENCE'))
        formDict['CareerPlans'] = str(request.form.get('CAREER_PLANS'))
        formDict['AspirationNext20Yrs'] = str(request.form.get('whysurf'))
        formDict['Mentor1'] = str(request.form.get('mentor0'))
        formDict['Mentor2'] = str(request.form.get('mentor1'))
        formDict['Mentor3'] = str(request.form.get('mentor2'))
        formDict['Mentor4'] = str(request.form.get('mentor3'))
        formDict['Mentor5'] = str(request.form.get('mentor4'))
        for i in range(0,26):
            if request.form['stitle'+''+str(i)] != '':
                formDict['stitle'+''+str(i)] = request.form['stitle'+''+str(i)]
                formDict['scredits'+''+str(i)] = request.form['scredits'+''+str(i)]
                formDict['sgrade'+''+str(i)] = request.form['sgrade'+''+str(i)]
                print('stitle'+''+str(i))
            else:
                break;
        mysql_dao.insertSecondForm(dbcon,formDict)
        session['user'] = formDict
    
        if request.form['submitButton'] == 'Submit Application':
            if request.form.get("agree") == "agree":

                formDict['ApplicationStatus'] = ApplicationStatus.ReferencesRequired.name 

                mysql_dao.insertSecondForm(dbcon,formDict)
                session['user'] = formDict
                ReferencesDict = dict()
                ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
                print(ReferencesDict)
                return render_template('third.html', ReferencesDict = ReferencesDict)
                
            else:
                error="Please accept terms and condition"
                mentorsList = mysql_dao.getMentorsList(dbcon)
                return flask.render_template('second.html', error=error,formDict=formDict,mentorsList=mentorsList)
        elif request.form['submitButton'] == 'Save':
            mentorsList = mysql_dao.getMentorsList(dbcon)
            return flask.render_template('second.html',formDict=formDict,mentorsList=mentorsList)
        elif request.form['submitButton'] == 'Back':
            universityList = mysql_dao.getUniversityList(dbcon)
            return flask.render_template('first.html',formDict=formDict,universityList=universityList)
        elif request.form['submitButton'] == 'Logout':
            session['logged_in']=False
            session.pop('user')
            return render_template('login.html')

@app.route('/submitThirdForm', methods=['GET', 'POST'])
def submitThirdForm():
  if request.method == 'POST':
    formDict = session['user']    #check with Shivani
    if request.form['submitButton'] == 'Submit':
      print('submit button pressed')
      for i in range(1,3):        ##check with shivani how may ref columns?
        formDict['RefName'+str(i)] = str(request.form.get('REFERENCE_'+str(i)))
        formDict['RefEmail'+str(i)] = str(request.form.get('ref'+str(i)+'email'))
        print(request.form.get('ref'+str(i)+'email'))
        toaddr = str(request.form.get('ref'+str(i)+'email'))        
        #sendEMail(toaddr)
      mysql_dao.insertThirdForm(dbcon,formDict)
      formDict['ReviewWaiver'] = str(request.form.get('REFERENCE_WAIVER'))
      print('Review Waiver'+formDict['ReviewWaiver'])
      session['user'] = formDict
      mysql_dao.insertReviewWaiver(dbcon, formDict)
      ReferencesDict = dict()
      ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
      #print(ReferencesDict)
      return render_template('third.html', ReferencesDict = ReferencesDict)      
    elif request.form['submitButton'] == 'Reset':
      print('reset button pressed')
      for i in range(0,2):        ##check with shivani how may ref columns?
        formDict['Name'] = str(request.form.get('REFERENCE_'+str(i)))
        print(formDict['Name'])
        formDict['Email'] = str(request.form.get('ref'+str(i)+'email'))
        print(formDict['Email'])
        mysql_dao.deleteThirdForm(dbcon,formDict)         #check with Chanda whether old referrer needs to be deleted
        ReferencesDict = dict()
        return render_template('third.html', ReferencesDict = ReferencesDict)          
    elif request.form['submitButton'] == 'Logout':
        print('logout')
        session['logged_in']=False
        session.pop('user')
        return render_template('login.html')

         

def sendEMail(toaddr):
  msg = MIMEMultipart()
  msg['From'] = "Amgen@biology.columbia.edu"
  msg['To'] = toaddr
  msg['Subject'] = "This is a test email"
  body = "Test email, please discard"
  msg.attach(MIMEText(body, 'plain'))
  server = smtplib.SMTP_SSL('send.columbia.edu', 587)
  server.login("Amgen@biology.columbia.edu", "744muDD")
  text = msg.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()
  
@app.route('/getStudentList', methods=['GET', 'POST'])
def getStudentList():
    if request.method == 'GET':
        studentList = mysql_dao.getStudentList(dbcon)        
        return render_template('studentList.html', studentList = studentList)
    elif request.method == 'POST':
        studentList = mysql_dao.getStudentList(dbcon)
        for row in studentList:
            if request.form['submitButton'] == row[0]:
                session['usernameProfile']='shivani'
                formDict=mysql_dao.getUser(dbcon,session['usernameProfile'])
                #print(formDict)
                universityList = mysql_dao.getUniversityList(dbcon)
                mentorsList = mysql_dao.getMentorsList(dbcon)
                return render_template('profile.html',formDict=formDict,universityList=universityList,mentorsList=mentorsList)


@app.route('/updateProfileByAdmin',methods=['POST'])
def updateProfileByAdmin():
    
    if request.form['submitButton'] == 'Back': 
        session.pop('usernameProfile')
        studentList = mysql_dao.getStudentList(dbcon)
        return render_template('studentList.html', studentList = studentList)
    elif request.form['submitButton'] == 'Logout':
        session.pop('usernameProfile')
        session['logged_in']=False
        return render_template('login.html')  
    
    if request.form['submitButton'] == 'Save':
        print("Inside save button")
        l=list()
        formDict=mysql_dao.getUser(dbcon,session['usernameProfile'])
        
        formDict['FirstName'] = str(request.form.get('FNAME'))
        formDict['LastName'] = str(request.form.get('LNAME'))
        formDict['DOB'] = str(request.form.get('DATEOFBIRTH'))
        formDict['Email'] = str(request.form.get('EMAIL'))
        formDict['AlternativeEmail'] = str(request.form.get('ALTERNATIVE_EMAIL'))
        formDict['Phone'] = str(request.form.get('PERMANENT_PHONE'))
        formDict['PermStreetAdr1'] = str(request.form.get('PERMANENT_ADDRESS1'))
        formDict['PermStreetAdr2'] = str(request.form.get('PERMANENT_ADDRESS2'))
        formDict['PermanentCity'] = str(request.form.get('PERMANENT_CITY'))
        formDict['PermanentState'] = str(request.form.get('PERMANENT_STATE'))
        formDict['PermanentZipCode'] = str(request.form.get('PERMANENT_ZIP'))
        formDict['CampusAdr1'] = str(request.form.get('SCHOOL_ADDRESS1'))
        formDict['CampusAdr2'] = str(request.form.get('SCHOOL_ADDRESS2'))
        formDict['CampusCity'] = str(request.form.get('CAMPUS_CITY'))
        formDict['CampusState'] = str(request.form.get('CAMPUS_STATE'))
        formDict['CampusZipCode'] = str(request.form.get('CAMPUS_ZIP'))
        formDict['HomeCity'] = str(request.form.get('HOMECITY'))
        formDict['HomeState'] = str(request.form.get('HOMESTATE'))
        formDict['Gender'] = str(request.form.get('GENDER'))      
        formDict['Ethnicity'] = str(request.form.get('ethinicity')) 
        if(formDict['Ethnicity']=='Other'):
          formDict["EthnicityOther"] = str(request.form.get('ethnicityother'))
        else:
          formDict["EthnicityOther"] = ""
        formDict['CitizenshipStatus'] = str(request.form.get('CITIZENSHIP'))
        if(formDict['CitizenshipStatus']=='resident'):
            formDict['PlaceOfBirth']=str(request.form.get('PLACEOFBIRTH'))
        formDict['MotherDegree'] = str(request.form.get('MOTHERDEGREE'))
        formDict['FatherDegree'] = str(request.form.get('FATHERDEGREE'))
        formDict['ClassCompletedSpring'] = str(request.form.get('CLASSCOMPLETE'))
        formDict['GraduationMonth'] = str(request.form.get('GRADUATION_DATE'))
        formDict['GraduationYear'] = str(request.form.get('BACHELORYEAR'))
        formDict['CumulativeGPA'] = str(request.form.get('CUMULATIVEGPA'))
        formDict['AdvancedDegreeObjective'] = str(request.form.get('ADVANCEDDEGREE'))
        if(formDict['AdvancedDegreeObjective']=='Other'):
            formDict['AdvancedDegreeObjectiveOther'] = str(request.form.get('ADVANCEDDEGREEOTHER'))
        formDict['IsUndergraduateResearchProgramOffered'] = str(request.form.get('RESEARCHOFFER'))
          
        if request.form.get('AMGENSITE'):
            l.append("Amgen National Website") 
        if request.form.get('UNIVERSITYSITE'):
            l.append("University website, University name")
            formDict['HowDidYouHearUniversityName'] = str(request.form.get('UNIVERSITYSITENAME'))
        else:
            formDict['HowDidYouHearUniversityName'] = ""
        if request.form.get('EMAILANNOUNCEMENT'):
            l.append("E-mail Announcement")
        if request.form.get('POSTER'):
            l.append("Poster")
        if request.form.get('CONFERENCE'):
            l.append("Conference, Conference Name")
            formDict['HowDidYouHearConferenceName'] = str(request.form.get('CONFERENCENAME'))
        else:
            formDict['HowDidYouHearConferenceName'] = ""
        if request.form.get('ACADEMICADVISOR'):
            l.append("Academic Advisor")
        if request.form.get('INTERNETSEARCH'):
            l.append("Internet Search")
        if request.form.get('HOMEUNIVERSITY'):
            l.append("Faculty/Staff from home university") 
        if request.form.get('OTHERUNIVERSITY'):
            l.append("Faculty/Staff from home university")
            formDict['HowDidYouHearOtherUniversityName'] = str(request.form.get('OTHERUNIVERSITYNAME'))
        else:
            formDict['HowDidYouHearOtherUniversityName'] = ""
        if request.form.get('AMGENOTHER'):
            l.append("Other")
            formDict['HowDidYouHearOther'] = str(request.form.get('AMGENOTHERNAME'))
        else:
            formDict['HowDidYouHearOther'] = ""
        formDict['HowDidYouHear'] = l
        
        formDict['AnyOtherAmgenScholarsSite'] = str(request.form.get('APPLYINGOTHER'))
        formDict['YesOtherAmgenScholarsSite'] = str(request.form.get('APPLYINGOTHERSPECIFY'))
        formDict['PastAmgenScholarParticipation'] = str(request.form.get('PARTICIPATED'))
        formDict['OriginalResearchPerformed'] = str(request.form.get('UG_RESEARCH'))
        formDict['CanArriveAtColumbiaMemorialDay'] = str(request.form.get('ARRIVEONFIRSTDAY'))
        formDict['ArriveAtColumbiaComments'] = str(request.form.get('ARRIVEONFIRSTDAYX'))
        formDict['CurrentlyAttendingUniversity'] = str(request.form.get('university'))
        formDict['Major'] = str(request.form.get('MAJOR'))
        formDict['DateSpringSemesterEnds'] = str(request.form.get('SEMESTER_END'))
        mysql_dao.insertFirstForm(dbcon,formDict)
        
        formDict['ScienceExperience'] = str(request.form.get('EXPERIENCE'))
        formDict['CareerPlans'] = str(request.form.get('CAREER_PLANS'))
        formDict['AspirationNext20Yrs'] = str(request.form.get('whysurf'))
        formDict['Mentor1'] = str(request.form.get('mentor0'))
        formDict['Mentor2'] = str(request.form.get('mentor1'))
        formDict['Mentor3'] = str(request.form.get('mentor2'))
        formDict['Mentor4'] = str(request.form.get('mentor3'))
        formDict['Mentor5'] = str(request.form.get('mentor4'))
        formDict['ApplicationStatus'] = str(request.form.get('ApplicationStatus'))
        for i in range(0,26):
            if request.form['stitle'+''+str(i)] != '':
                formDict['stitle'+''+str(i)] = request.form['stitle'+''+str(i)]
                formDict['scredits'+''+str(i)] = request.form['scredits'+''+str(i)]
                formDict['sgrade'+''+str(i)] = request.form['sgrade'+''+str(i)]
                print('stitle'+''+str(i))
            else:
                break;
        mysql_dao.insertSecondForm(dbcon,formDict)
        
        mentorsList = mysql_dao.getMentorsList(dbcon)
        universityList = mysql_dao.getUniversityList(dbcon)
        return render_template('profile.html',formDict=formDict,universityList=universityList,mentorsList=mentorsList)
    
def do_urlize(environment, value, trim_url_limit=None, nofollow=False):
    print('inside urilize')
    """Converts URLs in plain text into clickable links.

    If you pass the filter an additional integer it will shorten the urls
    to that number. Also a third argument exists that makes the urls
    "nofollow":

    .. sourcecode:: jinja

        {{ mytext|urlize(40, true) }}
            links are shortened to 40 chars and defined with rel="nofollow"
    """
    rv = urlize(value, trim_url_limit, nofollow)
    if environment.autoescape:
        rv = Markup(rv)
    return rv
    
if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(threaded=True)
  
def xstr(s):
    if s is None:
        return ''
    return str(s)

