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
    return render_template('third.html')
    '''
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        universityList = mysql_dao.getUniversityList(dbcon)
        return render_template('first.html',formDict=session['user'],universityList=universityList)
    '''

@app.route('/checkUsername', methods=['POST'])
def checkUsername():
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])
  
  formDict=mysql_dao.checkUser(dbcon,name,passwrd)
  
  if formDict['UserType'] == UserType.Student.name and formDict['ApplicationStatus'] == ApplicationStatus.IncompleteApplication.name:
      session['logged_in'] = True
      session['user'] = formDict
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('first.html',formDict=formDict,universityList=universityList)
  elif formDict['UserType'] == UserType.Student.name and formDict['ApplicationStatus'] == ApplicationStatus.UnderReview.name:
      session['logged_in'] = True
      session['user'] = formDict
      return render_template('third.html')
  elif formDict['UserType'] == UserType.Admin.name:
      session['logged_in'] = True
      formDict=mysql_dao.getUser(dbcon,'shivani')
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('profile.html',formDict=formDict,universityList=universityList)
  else:  
      flash('Wrong username or wrong password!')

  
@app.route('/addUsername', methods=['POST'])
def addUser():
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])

  user = mysql_dao.createNewUser(dbcon,name,passwrd,ApplicationStatus.IncompleteApplication.name)
  
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
        return render_template('first.html',formDict=dict(),universityList=universityList)
    elif request.form['submitButton'] == 'Logout':
        session['logged_in']=False
        session.pop('user')
        return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
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
                formDict['ApplicationStatus'] = ApplicationStatus.UnderReview.name 
                mysql_dao.insertSecondForm(dbcon,formDict)
                session['user'] = formDict
                return flask.render_template('third.html')
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
      for i in range(0,2):        ##check with shivani how may ref columns?
        formDict['RefName'+str(i)] = str(form.request.get('REFERENCE_'+str(i)))
        formDict['RefEmail'+str(i)] = str(form.request.get('ref'+str(i)+'email'))
        fromaddr = str(form.request.get('ref'+str(i)+'email'))        
        sendEMail(fromaddr)
      mysql_dao.insertThirdForm(dbcon,formDict)
      formDict['ReviewWaiver'] = str(form.request.get('REFERENCE_WAIVER'))
      session['user'] = formDict
      mysql_dao.insertReviewWaiver(dbcon, formDict)
      return sendEMailflask.render_template('third.html', formDict = formDict)
    elif request.form['submitBut'] == 'Reset':
      print('reset button pressed')
      for i in range(0,2):        ##check with shivani how may ref columns?
        formDict['Name'] = str(form.request.get('REFERENCE_'+str(i)))
        formDict['Email'] = str(form.request.get('ref'+str(i)+'email'))
        mysql_dao.deleteThirdForm(dbcon,formDict)         #check with Chanda whether old referrer needs to be deleted
        return flask.render_template('third.html')
    elif request.form['submitButton'] == 'Logout':
        session['logged_in']=False
        session.pop('user')
        return render_template('login.html')

def sendEMail(fromaddr):
  msg = MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = toaddr
  msg['Subject'] = ""
  body = ""
  msg.attach(MIMEText(body, 'plain'))
  server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
  server.login(toaddr, "########")
  text = msg.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()

if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(threaded=True)
  
def xstr(s):
    if s is None:
        return ''
    return str(s)

