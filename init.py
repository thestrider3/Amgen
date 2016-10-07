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
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('first.html')

@app.route('/checkUsername', methods=['POST'])
def checkUsername():
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])
  
  user=mysql_dao.checkUser(dbcon,name,passwrd)
 
  if user:
      session['logged_in'] = True
      userSession.add(user)
      render_template('first.html')
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
      session['user'] = json.dumps(user.__dict__)
      temp = json.loads(session['user']);
      print(session['logged_in'])
      print(session['user'])
      print(temp["username"])
      return render_template('first.html')
  else:
       flash("Username already exists. Please try again.")
      
      
'''@app.route('/submitFirstForm', methods=['POST'])
def addFirstForm():
  #userid = os.urandom(24)

  formDict = dict()
  mysql_dao.createNewUser(dbcon,,d)
  user = User(name,passwrd,True);
  login_user(user)
  next = flask.request.args.get('next')
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
    formDict['HowDidYouHear'] = 
  if request.form.get('UNIVERSITYSITE'):
    formDict['HowDidYouHear'] = 
    formDict['HeardUniversityName'] = 
  if request.form.get('EMAILANNOUNCEMENT'):
    formDict['HowDidYouHear'] = 
  if request.form.get('POSTER'):
    formDict['HowDidYouHear'] =
  if request.form.get('CONFERENCE'):
    CONFERENCENAME
    formDict['HowDidYouHear'] =
  if request.form.get('ACADEMICADVISOR'):
    formDict['HowDidYouHear'] =
  if request.form.get('INTERNETSEARCH'):
    formDict['HowDidYouHear'] = 
  if request.form.get('HOMEUNIVERSITY'):
    formDict['HowDidYouHear'] = 
  if request.form.get('OTHERUNIVERSITY'):
    OTHERUNIVERSITYNAME
    formDict['HowDidYouHear'] =  
  if request.form.get('AMGENOTHER'):
    formDict['HowDidYouHear'] = 
    AMGENOTHERNAME
  


  formDict['AnyOtherAmgenScholarsSite'] = str(request.form['APPLYINGOTHER'])
  formDict['YesOtherAmgenScholarsSite'] = str(request.form['APPLYINGOTHERSPECIFY'])
  formDict['PastAmgenScholarParticipation'] = str(request.form['PARTICIPATED'])
  formDict['OriginalResearchPerformed'] = str(request.form['UG_RESEARCH'])
  formDict['CanArriveAtColumbiaMemorialDay'] = str(request.form['ARRIVEONFIRSTDAY'])
  formDict['ArriveAtColumbiaComments'] = str(request.form['ARRIVEONFIRSTDAYX'])
  formDict['CurrentlyAttendingUniversity'] = str(request.form['university'])
  formDict['Major'] = str(request.form['MAJOR'])
  formDict['DateSpringSemesterEnds'] = str(request.form['SEMESTER_END'])

    
return flask.render_template('first.html')
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # file upload handler code will be here
  if request.method == 'POST':
      file = request.files['file']
      extension = os.path.splitext(file.filename)[1]
      f_name = str(uuid.uuid4()) + extension
      app.config['UPLOAD_FOLDER'] = 'static/Uploads'
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
  return json.dumps({'filename':f_name})

if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(threaded=True)

