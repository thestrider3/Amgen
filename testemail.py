import smtplib, os, json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, request, render_template, g, redirect, Response

fromaddr = "tulikasbhatt@gmail.com"
toaddr = "tulikabhatt92@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Python email"
body = "Python test mail"
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
#server.login(gmail_user, password)
#server.sendmail(gmail_user, TO, BODY)
#server = smtplib.SMTP('smtp.gmail.com', 587)
#server.ehlo()
#server.starttls()
#server.ehlo()
server.login("tulikasbhatt@gmail.com", "Linkin@park13")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

#python server.py --help