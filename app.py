from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('login.html')

@app.route('/addUsername', methods=['POST','GET'])
def addUsername():
  #print("hhhhhh")
  if request.method == 'POST':
  	print(request.form['userid'])
  	return json.dumps({'filename':request.form['userid']})

if __name__ == "__main__":
    app.run()
