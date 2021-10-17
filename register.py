from flask import Flask,render_template, url_for,request,session,redirect
from pymongo import MongoClient
import bcrypt
from datetime import datetime


app = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)

@app.route('/')
def index():
  if 'username' in session:
    return 'you are logged in as' + session['username']
  
  return render_template('register.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    existing_user = users.find_one({'name': request.form['username']})

    if existing_user is None:
      hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
      users.insert_one({'date': datetime.date,'name': request.form['username'], 'password':hashpass, 'email': request.form['email'], 'phonenumber': request.form['phonenumber'], 'labor':request.form['keywords']})
      session['username'] = request.form['username']
      return redirect(url_for('index'))

    return 'Username already exists'
  return render_template('register.html')


  return ''



if __name__ == '__main__':
  app.secret_key = 'mysecret'
  app.run(debug=True)
