#!/usr/bin/env python2.7

import os, uuid, json

from flask import Flask, request, render_template, g, redirect, Response
from mysql_dao import createDatabaseConnection, createNewUser

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
dbcon=''

@app.before_request
def before_request():
  global dbcon
  dbcon = createDatabaseConnection()

@app.teardown_request
def teardown_request(exception):
  global dbcon
  try:
    dbcon.close()
  except Exception as e:
    pass

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/addUsername', methods=['POST'])
def add():
  name = str(request.form['userid'])
  passwrd = str(request.form['passwsrd'])
  print(name)
  print(passwrd)
  createNewUser(dbcon,name,passwrd)
  return render_template("first.html")


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


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  app.run()

