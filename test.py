#!/usr/bin/env python2.7

import os, uuid, json,flask
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from flask import Flask, request, render_template, g, redirect, Response

def sendEMail(toaddr):
  msg = MIMEMultipart()
  msg['From'] = "Amgen@biology.columbia.edu"
  msg['To'] = toaddr
  msg['Subject'] = "This is a test email"
  body = "Test email, please discard"
  msg.attach(MIMEText(body, 'plain'))
  
  server = smtplib.SMTP('biomail.biology.columbia.edu', 587)
  server.starttls()
  server.ehlo()
  server.login("Amgen@biology.columbia.edu", "744BmuDD")
  text = msg.as_string()
  server.set_debuglevel(True)
  server.sendmail(fromaddr, toaddr, text)
  server.quit()
  
if __name__ == "__main__":
    sendEMail('shivani.b.gupta@gmail.com')