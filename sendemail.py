import smtplib, os, json, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

@app.route('/')
def main():
    return render_template('third.html')

@app.route('/sendEmail', methods=['POST'])
def sendEmail():
  print("hhhhhh")
  if request.method == 'POST':
    fromaddr = "tulikasbhatt@gmail.com"
    toaddr = request.form['ref1email']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Python email"
    print("The email address is '" + toaddr + "'")
    #msg['Subject'] = "Python email"
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
    return json.dumps({'filename':request.form['ref1email']})

if __name__ == "__main__":
  import click  
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):    
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()

#python server.py --help