#!/usr/bin/env python2.7

from werkzeug.utils import secure_filename
import os, uuid, json, flask, mysql_dao, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, request, flash, render_template, session, abort, g, redirect 
from flask import Response, send_from_directory, url_for 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from user import *
from applicationStatus import ApplicationStatus
from referenceStatus import ReferenceStatus
from userType import UserType
import utils

UPLOAD_FOLDER = '/home/shivani/Documents/tulika/amgen/files'
UPLOAD_REF_FOLDER = '/home/shivani/Documents/tulika/amgen/refFiles'
ALLOWED_EXTENSIONS = set(['pdf'])
#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_REF_FOLDER'] = UPLOAD_REF_FOLDER

def saveFile(transcript,username,typeFile,referalName=""):     
    if typeFile == 'Transcript':
        folder= app.config['UPLOAD_FOLDER']
        filename = secure_filename(username+".pdf")
    elif typeFile == 'Referal':
        folder= app.config['UPLOAD_REF_FOLDER']
        filename = secure_filename(username+" "+referalName+".pdf")
    if transcript:
        if allowed_file(transcript.filename):
            transcript.save(os.path.join(folder, filename))
            return filename
        
    
def count_letters(word):
  count = 0
  for c in word:
      count += 1
  return count


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
    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        formDict = session['user']
        if formDict['UserType'] == UserType['Student'] :
          if formDict['ApplicationStatus'] == ApplicationStatus['IncompleteApplication']:
              universityList = mysql_dao.getUniversityList(dbcon)
              return render_template('first.html',formDict=formDict,universityList=universityList)
          elif formDict['ApplicationStatus'] == ApplicationStatus['ReferencesRequired2'] or formDict['ApplicationStatus'] == ApplicationStatus['ReferencesRequired1']:
              ReferencesDict = dict()
              ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
              return render_template('third.html', ReferencesDict = ReferencesDict)  
          elif formDict['ApplicationStatus'] == ApplicationStatus['UnderReview']:
              return render_template('underReview.html')
      
        elif formDict['UserType'] == UserType['Admin']:
          studentList = mysql_dao.getStudentList(dbcon)
          return render_template('studentList.html',studentList=studentList)
    

@app.route('/checkUsername', methods=['POST'])
def checkUsername():
  
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])

  formDict=mysql_dao.checkUser(dbcon, name, passwrd)
  
  if not formDict:
      return render_template('login.html',error="Username or password is incorrect. Please try again.")
  if not 'HowDidYouHear' in formDict:
      formDict['HowDidYouHear']=''
      
  session['logged_in'] = True
  session['user']=formDict

  if formDict['UserType'] == UserType['Student']: 
      if formDict['ApplicationStatus'] == ApplicationStatus['IncompleteApplication']:
          universityList = mysql_dao.getUniversityList(dbcon)          
          return render_template('first.html',formDict=formDict,universityList=universityList)
          
      elif formDict['ApplicationStatus'] == ApplicationStatus['ReferencesRequired2'] or formDict['ApplicationStatus'] == ApplicationStatus['ReferencesRequired1']:
          ReferencesDict = dict()
          ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
          return render_template('third.html', ReferencesDict = ReferencesDict)  
      elif formDict['ApplicationStatus'] == ApplicationStatus['UnderReview']:
          return render_template('underReview.html')
  elif formDict['UserType'] == UserType['Admin']:
      studentList = mysql_dao.getStudentList(dbcon)
      return render_template('studentList.html',studentList=studentList)
  elif formDict['UserType'] == UserType['Referal']:
      studentList = mysql_dao.getStudentsByProf(dbcon,formDict['Username'])
      if not studentList:
          return render_template('referalStudentList.html',studentList=studentList,message="References no longer required")
      return render_template('referalStudentList.html',studentList=studentList)

  
@app.route('/addUsername', methods=['POST'])
def addUser():
  global userSession
  name = str(request.form['username'])
  passwrd = str(request.form['passwrd'])
  if ".edu" not in name:
      return render_template('signup.html',error="Username must be an email and ending in .edu")
      
  user = mysql_dao.createNewUser(dbcon,name,passwrd,ApplicationStatus['IncompleteApplication'],UserType['Student'])

  if user:
      session['logged_in'] = True
      session['user'] = user
      universityList = mysql_dao.getUniversityList(dbcon)
      return render_template('first.html',formDict=dict(),universityList=universityList)
  else:
       return render_template('signup.html',error="Username already exists. Please try again.")
      
      
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
        if not ( formDict['FirstName'] and
            formDict['LastName'] and
            formDict['DOB'] and
            formDict['Email'] and
            formDict['AlternativeEmail'] and
            formDict['Phone'] and
            formDict['PermStreetAdr1'] and
            formDict['PermanentCity'] and
            formDict['PermanentState'] and
            formDict['PermanentZipCode'] and
            formDict['CampusAdr1'] and
            formDict['CampusCity'] and
            formDict['CampusState'] and
            formDict['CampusZipCode'] and
            formDict['HomeCity'] and
            formDict['HomeState'] and
            formDict['Gender'] and
            formDict['Ethnicity'] and
            formDict['CitizenshipStatus'] and
            formDict['MotherDegree'] and
            formDict['FatherDegree'] and
            formDict['ClassCompletedSpring'] and
            formDict['GraduationMonth'] and
            formDict['GraduationYear'] and
            formDict['CumulativeGPA'] and
            formDict['AdvancedDegreeObjective'] and
            formDict['HowDidYouHear'] and
            formDict['IsUndergraduateResearchProgramOffered'] and
            formDict['AnyOtherAmgenScholarsSite'] and
            formDict['PastAmgenScholarParticipation'] and
            formDict['OriginalResearchPerformed'] and
            formDict['CanArriveAtColumbiaMemorialDay'] and
            formDict['CurrentlyAttendingUniversity'] and
            formDict['Major'] and
            formDict['DateSpringSemesterEnds'] ):
            universityList = mysql_dao.getUniversityList(dbcon)
            return render_template('first.html',formDict=formDict,universityList=universityList,error="Please complete all fields before submitting")   
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
        session['logged_in'] = True
        formDict = session['user']
        formDict['ScienceExperience'] = str(request.form.get('EXPERIENCE'))
        formDict['CareerPlans'] = str(request.form.get('CAREER_PLANS'))
        formDict['Mentor1'] = str(request.form.get('mentor0'))
        formDict['Mentor2'] = str(request.form.get('mentor1'))
        formDict['Mentor3'] = str(request.form.get('mentor2'))
        formDict['Mentor4'] = str(request.form.get('mentor3'))
        formDict['Mentor5'] = str(request.form.get('mentor4'))
        formDict['Mentor6'] = ''
        formDict['Mentor7'] = ''
        formDict['Mentor8'] = ''
        for i in range(0,26):
            if request.form['stitle'+''+str(i)] != '':
                formDict['stitle'+''+str(i)] = request.form['stitle'+''+str(i)]
                formDict['scredits'+''+str(i)] = request.form['scredits'+''+str(i)]
                formDict['sgrade'+''+str(i)] = request.form['sgrade'+''+str(i)]                
            else:
                break;
        
        transcript = request.files.get('fileupload')
        formDict['Transcript'] = saveFile(transcript,formDict['Username'],'Transcript')
        
    
        if request.form['submitButton'] == 'Submit Application':
            error = ""  
            if not formDict['Transcript']:        
                error = "Please select a pdf file"
                
            if not request.form.get("agree") == "agree":
                error = "Please accept terms and condition" 
            
            if count_letters(formDict['ScienceExperience']) > 700:
                    error="Character Limit exceeded for science experience."
                    
            if count_letters(formDict['CareerPlans']) > 500:
                error="Character Limit exceeded for career plans."
                
            if not (formDict['ScienceExperience'] and \
                    formDict['CareerPlans'] and \
                    formDict['Mentor1'].strip() and \
                    formDict['Mentor2'].strip() and \
                    formDict['Mentor3'].strip() and \
                    formDict['Mentor4'].strip() and \
                    formDict['Mentor5'].strip()):
                error="Please complete all fields before submitting."   

            
            if not error:
                formDict['ApplicationStatus'] = ApplicationStatus['ReferencesRequired2']
                mysql_dao.insertSecondForm(dbcon,formDict)
                session['user'] = formDict
                ReferencesDict = dict()
                ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
                return render_template('third.html', ReferencesDict = ReferencesDict)
                
            else:
                mentorsList = mysql_dao.getMentorsList(dbcon)       
                return flask.render_template('second.html', error=error,formDict=formDict,mentorsList=mentorsList)

        elif request.form['submitButton'] == 'Back':
            universityList = mysql_dao.getUniversityList(dbcon)
            return flask.render_template('first.html',formDict=formDict,universityList=universityList)
            
        elif request.form['submitButton'] == 'Logout':
            session['logged_in']=False
            session.pop('user')
            return render_template('login.html')
            
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/submitThirdForm', methods=['GET', 'POST'])
def submitThirdForm():
  if request.method == 'POST':
    formDict = session['user']    
    if request.form['submitButton'] == 'Submit':
      for i in range(1,3):        
        formDict['RefName'+str(i)] = str(request.form.get('REFERENCE_'+str(i)))
        formDict['RefEmail'+str(i)] = str(request.form.get('ref'+str(i)+'email'))
        if not (formDict['RefName'+str(i)] and formDict['RefEmail'+str(i)]):
            error="Please fill in all the  reference details."
            return render_template('third.html', ReferencesDict = formDict,error=error)     
        toaddr = str(request.form.get('ref'+str(i)+'email'))        
      formDict['ReviewWaiver'] = str(request.form.get('REFERENCE_WAIVER'))
      
      if not (formDict['ReviewWaiver']):
            ReferencesDict = dict()
            error="Please select option for review waver."
            return render_template('third.html', ReferencesDict = ReferencesDict,error=error)
      
      session['user'] = formDict
      newRefs = mysql_dao.insertThirdForm(dbcon,formDict)
      mysql_dao.insertReviewWaiver(dbcon, formDict)

      for ref in newRefs:
          utils.sendEmail(ref[0],ref[1],formDict['FirstName']+" "+formDict["LastName"],ref[2])
      
      ReferencesDict = dict()
      ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
      return render_template('third.html', ReferencesDict = ReferencesDict,message="References have been submitted. You can modify them by logging again later also.")      

    elif request.form['submitButton'] == 'Reset':
      for i in range(0,2):
        formDict['Name'] = str(request.form.get('REFERENCE_'+str(i)))
        formDict['Email'] = str(request.form.get('ref'+str(i)+'email'))
        ReferencesDict = dict()
        return render_template('third.html', ReferencesDict = ReferencesDict)
          
    elif request.form['submitButton'] == 'Logout':
        session['logged_in']=False
        session.pop('user')
        return render_template('login.html')


@app.route('/getReferalStudentList',methods=['POST'])
def getReferalStudentList():
    i=0
    if request.method == 'POST' and request.form['submitButton'] == 'Submit':
        formDict=session['user']
        studentList = mysql_dao.getStudentsByProf(dbcon,formDict['Username'])
        
        for row in studentList:
            referal = request.files.get('fileupload'+row[0])
            temp= saveFile(referal,row[0],'Referal',formDict['Username'])
            if temp:
                formDict['Referal'+str(i)] = row[0]
                formDict['ReferalPath'+str(i)] = temp
                i=i+1
        if i>0:
            mysql_dao.reflectReferalSubmitted(dbcon,formDict)
                
        return render_template('referalStudentList.html',studentList=studentList,message1='Reference Submission was successful.')
    elif request.method == 'POST' and request.form['submitButton'] == 'Logout':
        session.pop('user')
        session['logged_in']=False
        return render_template('login.html')
    
    
@app.route('/getStudentList', methods=['GET', 'POST'])
def getStudentList():
    if request.method == 'GET':
        studentList = mysql_dao.getStudentList(dbcon)        
        return render_template('studentList.html', studentList = studentList)
    elif request.method == 'POST':
        if request.form['submitButton'] == 'Logout':
            session['logged_in']=False
            return render_template('login.html')
        studentList = mysql_dao.getStudentList(dbcon)
        for row in studentList:
            if request.form['submitButton'] == row[0]:
                session['usernameProfile']=row[0]
                formDict=mysql_dao.getUser(dbcon,session['usernameProfile'])
                ReferencesDict = dict()
                #print(formDict)
                ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
                universityList = mysql_dao.getUniversityList(dbcon)
                mentorsList = mysql_dao.getMentorsList(dbcon)
                return render_template('profile.html',formDict=formDict,universityList=universityList,mentorsList=mentorsList,ReferencesDict=ReferencesDict)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

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
        
    elif request.form['submitButton'] =='View':
        #filename = mysql_dao.getTranscript(dbcon,session['usernameProfile'])
        print('View Transcript')
        fn = str(session['usernameProfile'])
        i = fn.index('@')
        fn = fn[:i]
        filename = secure_filename(fn+".pdf")
        print(filename)      
        return redirect(url_for('uploaded_file',filename=filename))
        
    
    if request.form['submitButton'] == 'Save':
        l=list()
        formDict=dict()
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
        formDict['Mentor1'] = str(request.form.get('mentor0'))
        formDict['Mentor2'] = str(request.form.get('mentor1'))
        formDict['Mentor3'] = str(request.form.get('mentor2'))
        formDict['Mentor4'] = str(request.form.get('mentor3'))
        formDict['Mentor5'] = str(request.form.get('mentor4'))
        formDict['Mentor6'] = str(request.form.get('mentor5'))
        formDict['Mentor7'] = str(request.form.get('mentor6'))
        formDict['Mentor8'] = str(request.form.get('mentor7'))
        formDict['ApplicationStatus'] = str(request.form.get('ApplicationStatus'))
        for i in range(0,26):
            if request.form['stitle'+''+str(i)] != '':
                formDict['stitle'+''+str(i)] = request.form['stitle'+''+str(i)]
                formDict['scredits'+''+str(i)] = request.form['scredits'+''+str(i)]
                formDict['sgrade'+''+str(i)] = request.form['sgrade'+''+str(i)]
            else:
                break;
        
                
        error = ""     
        
        transcript = request.files.get('fileupload')
        formDict['Transcript']=saveFile(transcript,session['usernameProfile'],'Transcript')
    
        mysql_dao.insertSecondForm(dbcon,formDict)
        
        
        for i in range(1,3):       
            formDict['RefName'+str(i)] = str(request.form.get('REFERENCE_'+str(i)))
            formDict['RefEmail'+str(i)] = str(request.form.get('ref'+str(i)+'email'))
            formDict['RefFilePath'+str(i)] = session['usernameProfile']+' '+formDict['RefName'+str(i)] +'.pdf'
          
        
        formDict['ReviewWaiver'] = str(request.form.get('REFERENCE_WAIVER'))
        session['user'] = formDict
        mysql_dao.insertThirdForm(dbcon,formDict)
        mysql_dao.insertReviewWaiver(dbcon, formDict)

        #formDict['Transcript'] = request.files['fileupload'].read()
              
        
        mentorsList = mysql_dao.getMentorsList(dbcon)
        universityList = mysql_dao.getUniversityList(dbcon)

        ReferencesDict = dict()
        ReferencesDict = mysql_dao.getReferences(dbcon, formDict)
        
        ref1 = request.files.get('fileupload1')
        temp = saveFile(ref1,session['usernameProfile'],'Referal',formDict['RefEmail1'])
        if temp:
            formDict['RefFilePath1']=temp
        
        
        ref2 = request.files.get('fileupload2')
        temp = saveFile(ref2,session['usernameProfile'],'Referal',formDict['RefEmail2'])
        if temp:
            formDict['RefFilePath2']=temp
        
        return render_template('profile.html',formDict=formDict,universityList=universityList,mentorsList=mentorsList,ReferencesDict=ReferencesDict)

    
if __name__ == "__main__":
  app.secret_key = os.urandom(24)
  app.run(threaded=True)
  
def xstr(s):
    if s is None:
        return ''
    return str(s)

