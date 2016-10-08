#!/usr/bin/env python2.7

import os, uuid, json,flask,mysql_dao

from flask import Flask, request, flash, render_template, session, abort, g, redirect, Response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from user import *
import json

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__)


@app.before_request
def before_request():
    global dbcon,engine,userSession
    dbcon,engine = mysql_dao.createDatabaseConnection()
    Session = sessionmaker(bind=engine)
    userSession = Session()

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
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])
  
  formDict=mysql_dao.checkUser(dbcon,name,passwrd)
 
  if formDict:
      print formDict
      session['logged_in'] = True
      session['user'] = formDict
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('first.html',formDict=formDict,universityList=universityList)
  else:  
      flash('Wrong username or wrong password!')

  
@app.route('/addUsername', methods=['POST'])
def addUser():
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])
  print(name)
  print(passwrd)

  user = mysql_dao.createNewUser(dbcon,name,passwrd)
  
  if user:
      print("successfully created user")
      session['logged_in'] = True
      session['user'] = user
      print(session['logged_in'])
      print(session['user'])
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('first.html',formDict=dict(),universityList=universityList)
  else:
       flash("Username already exists. Please try again.")
      
      
@app.route('/submitFirstForm', methods=['POST'])
def addFirstForm():
  print("inside submit first form")
  #userid = os.urandom(24)
  l=list()
  formDict=session['user']
  #user = User(name,passwrd,True);
  #login_user(user)
  #next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url

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
  #mysql_dao.createNewUser(dbcon,,formDict) 
  return flask.render_template('second.html')


'''
@app.route('/submitFirstForm', methods=['POST'])
def addSecondForm():
if request.form['submitBut'] == 'Next':
  return flask.render_template('third.html')
'''    

#@app.route('/upload', methods=['GET', 'POST'])

#@app.route('/submitFirstForm', methods=['POST'])
#def addSecondForm():

    




@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    formDict = dict()
    if request.form['submitBut'] == 'Next':
      formDict['ScienceExperience'] = str(request.form.get('EXPERIENCE'))
      formDict['CareerPlans'] = str(request.form.get('CAREER_PLANS')
      formDict['AspirationNext20Yrs'] = str(request.form.get('whysurf'))
      formDict['Mentor1'] = str(request.form.get('mentor0'))
      formDict['Mentor2'] = str(request.form.get('mentor1'))
      formDict['Mentor3'] = str(request.form.get('mentor2'))
      formDict['Mentor4'] = str(request.form.get('mentor3'))
      formDict['Mentor5'] = str(request.form.get('mentor4'))

      #file = request.files['fileupload']
      #formDict['Transcript'] = open('file', 'rb').read()
      #formDict['Transcript'] = str(request.form['fileupload'])
      if request.form.get("agree") == "agree":
        if request.form['submitBut'] == 'Next':
          formDict['IsApplicationSubmitted'] = "Y" 
          mysql_dao.insertSecondForm(dbcon,"tb",formDict)
          for i in range(0,26):
            if request.form['stitle'+''+str(i)] != '':
              formDict['stitle'+''+str(i)] = request.form['stitle'+''+str(i)]
              formDict['scredits'+''+str(i)] = request.form['scredits'+''+str(i)]
              formDict['sgrade'+''+str(i)] = request.form['sgrade'+''+str(i)]
              print('stitle'+''+str(i))
              mysql_dao.insertStudentCourse(dbcon, "tb", formDict, 'stitle'+''+str(i), 'scredits'+''+str(i), 'sgrade'+''+str(i))
          return flask.render_template('third.html')
      else:
        error="Please accept terms and condition"
        return flask.render_template('second.html', error=error)
      if request.form['submitBut'] == 'Back':
        return flask.render_template('first.html')


  


if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(threaded=True)
  
def xstr(s):
    if s is None:
        return ''
    return str(s)

