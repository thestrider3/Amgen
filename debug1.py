from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('login.html')

@app.route('/addUsername',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
		result = request.form['Name']
		print(result)
		return render_template('login.html')
if __name__ == '__main__':
   app.run(debug = True)