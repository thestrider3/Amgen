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
    login_manager.init_app(app)
    return render_template('login.html')

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


@app.route('/upload', methods=['GET', 'POST'])
@login_required
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
  app.run()

