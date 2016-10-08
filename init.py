#!/usr/bin/env python2.7

import os, uuid, json,flask,mysql_dao

from flask import Flask, request, render_template, g, redirect, Response
from flask_login import LoginManager,login_required,login_user
from user import *

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
dbcon=''
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return mysql_dao.getUser(dbcon,user_id)
  
@app.before_request
def before_request():
  global dbcon
  dbcon = mysql_dao.createDatabaseConnection()
  
  

@app.teardown_request
def teardown_request(exception):
  global dbcon
  try:
    dbcon.close()
  except Exception as e:
    pass

@app.route('/')
def main():
    #login_manager.init_app(app)
    return render_template('second.html')

@app.route('/addUsername', methods=['POST'])
def add():
  name = str(request.form['userid'])
  passwrd = str(request.form['passwrd'])
  userid = os.urandom(24)
  print(userid)
  print(name)
  print(passwrd)
  mysql_dao.createNewUser(dbcon,name,userid,passwrd)
  user = User(name,passwrd,True);
  login_user(user)
  next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url

  return flask.render_template('first.html')

@app.route('/submitFirstForm', methods=['POST'])
def addFirstForm():
  #userid = os.urandom(24)
  l=list()
  formDict = dict()
  
  #user = User(name,passwrd,True);
  #login_user(user)
  #next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url

  formDict['FirstName'] = str(request.form['FNAME'])
  formDict['LastName'] = str(request.form['LNAME'])
  formDict['DOB'] = str(request.form['DATEOFBIRTH'])
  formDict['Email'] = str(request.form['EMAIL'])
  formDict['AlternativeEmail'] = str(request.form['ALTERNATIVE_EMAIL'])
  formDict['Phone'] = str(request.form['PERMANENT_PHONE'])
  formDict['PermStreetAdr1'] = str(request.form['PERMANENT_ADDRESS1'])
  formDict['PermStreetAdr2'] = str(request.form['PERMANENT_ADDRESS2'])
  formDict['PermanentCity'] = str(request.form['PERMANENT_CITY'])
  formDict['PermanentState'] = str(request.form['PERMANENT_STATE'])
  formDict['PermanentZipCode'] = str(request.form['PERMANENT_ZIP'])
  formDict['CampusAdr1'] = str(request.form['SCHOOL_ADDRESS1'])
  formDict['CampusAdr2'] = str(request.form['SCHOOL_ADDRESS2'])
  formDict['CampusCity'] = str(request.form['CAMPUS_CITY'])
  formDict['CampusState'] = str(request.form['CAMPUS_STATE'])
  formDict['CampusZipCode'] = str(request.form['CAMPUS_ZIP'])
  formDict['HomeCity'] = str(request.form['HOMECITY'])
  formDict['UserId'] = str(request.form['HOMESTATE'])
  formDict['Gender'] = str(request.form['GENDER'])   
  formDict['Ethnicity'] = str(request.form['ethinicity'])  
  formDict['CitizenshipStatus'] = str(request.form['CITIZENSHIP'])
  formDict['MotherDegree'] = str(request.form['MOTHERDEGREE'])
  formDict['FatherDegree'] = str(request.form['FATHERDEGREE'])
  formDict['ClassCompletedSpring'] = str(request.form['CLASSCOMPLETE'])
  formDict['GraduationMonth'] = str(request.form['GRADUATION_DATE'])
  formDict['GraduationYear'] = str(request.form['BACHELORYEAR'])
  formDict['CumulativeGPA'] = str(request.form['CUMULATIVEGPA'])
  formDict['AdvancedDegreeObjective'] = str(request.form['ADVANCEDDEGREE'])
  formDict['IsUndergraduateResearchProgramOffered'] = str(request.form['RESEARCHOFFER'])
  if request.form.get('AMGENSITE'):
    l.append("Amgen National Website") 
  if request.form.get('UNIVERSITYSITE'):
    l.append("University website, University name")
    formDict['HowDidYouHearUniversityName'] = str(request.form[UNIVERSITYSITENAME])
  else:
    formDict['HowDidYouHearUniversityName'] = ""
  if request.form.get('EMAILANNOUNCEMENT'):
    l.append("E-mail Announcement")
  if request.form.get('POSTER'):
    l.append("Poster")
  if request.form.get('CONFERENCE'):
    l.append("Conference, Conference Name")
    formDict['HowDidYouHearConferenceName'] = str(request.form[CONFERENCENAME])
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
    formDict['HowDidYouHearOtherUniversityName'] = str(request.form[OTHERUNIVERSITYNAME])
  else:
    formDict['HowDidYouHearOtherUniversityName'] = ""
  if request.form.get('AMGENOTHER'):
    l.append("Other")
    formDict['HowDidYouHearOther'] = str(request.form[AMGENOTHERNAME])
  else:
    formDict['HowDidYouHearOther'] = ""
  formDict['HowDidYouHear'] = l
  formDict['AnyOtherAmgenScholarsSite'] = str(request.form['APPLYINGOTHER'])
  formDict['YesOtherAmgenScholarsSite'] = str(request.form['APPLYINGOTHERSPECIFY'])
  formDict['PastAmgenScholarParticipation'] = str(request.form['PARTICIPATED'])
  formDict['OriginalResearchPerformed'] = str(request.form['UG_RESEARCH'])
  formDict['CanArriveAtColumbiaMemorialDay'] = str(request.form['ARRIVEONFIRSTDAY'])
  formDict['ArriveAtColumbiaComments'] = str(request.form['ARRIVEONFIRSTDAYX'])
  formDict['CurrentlyAttendingUniversity'] = str(request.form['university'])
  formDict['Major'] = str(request.form['MAJOR'])
  formDict['DateSpringSemesterEnds'] = str(request.form['SEMESTER_END'])
  mysql_dao.insertFirstForm(dbcon,"tb",formDict)
  #mysql_dao.createNewUser(dbcon,,formDict) 
  return flask.render_template('first.html')

#@app.route('/submitFirstForm', methods=['POST'])
#def addSecondForm():

    




@app.route('/upload', methods=['GET', 'POST'])
#@login_required
def upload():
  if request.method == 'POST':
    formDict = dict()
    if request.form['submitBut'] == 'Next':
      formDict['ScienceExperience'] = str(request.form['EXPERIENCE'])
      formDict['CareerPlans'] = str(request.form['CAREER_PLANS'])
      formDict['AspirationNext20Yrs'] = str(request.form['whysurf'])
      formDict['Mentor1'] = str(request.form['mentor0'])
      formDict['Mentor2'] = str(request.form['mentor1'])
      formDict['Mentor3'] = str(request.form['mentor2'])
      formDict['Mentor4'] = str(request.form['mentor3'])
      formDict['Mentor5'] = str(request.form['mentor4'])

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
  app.run()

