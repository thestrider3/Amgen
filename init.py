#!/usr/bin/env python2.7

import os, uuid, json
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "mysql+mysqlconnector://aheicklen:mass67@mysql.columbiasurf.dreamhosters.com:3306/columbiasurf" 
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/addUsername', methods=['POST'])
def add():
  name = str(request.form['userid'])
  passwrd = str(request.form['passwrd'])
  print(name)
  print(passwrd)
  g.conn.execute('INSERT INTO login_info VALUES (%s, %s)', [name,passwrd])
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

