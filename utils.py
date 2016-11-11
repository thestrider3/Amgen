# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:31:00 2016

@author: shivani
"""
from enums import emailMessages
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

messageType={'ReferenceRequest':'ReferenceRequest'}


def sendRecommendationRequestEmail(toProf,profName,fromStud,profPassword):
  msg = MIMEMultipart()
  msg['To'] = toProf
  
  msg['Subject'] = "Letter of Recommendation Requested By "+fromStud
  body = emailMessages['recommenderRequestMail'].format(profName=profName,studentName=fromStud,username=toProf,password=profPassword)
  
  msg['From'] = "Amgen@biology.columbia.edu"
  msg.attach(MIMEText(body, 'plain'))
  fromaddr = 'Amgen@biology.columbia.edu'
  server = smtplib.SMTP('biomail.biology.columbia.edu', 587)
  server.starttls()
  server.ehlo()
  server.login("Amgen@biology.columbia.edu", "744muDD")
  text = msg.as_string()
  server.set_debuglevel(True)
  server.sendmail(fromaddr, toProf, text)
  server.quit()