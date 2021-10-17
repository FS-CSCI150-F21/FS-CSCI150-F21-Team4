from flask import Flask,render_template, url_for,request,session,redirect
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)

def index():
  if 'username' in session:
    return 'you are logged in as' + session['username']
  
  return render_template('register.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    users = mongo.db.userRegistration
    existing_user = user.find_one({'name': request.form{'username'}})

    if existing_user is None:
      hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
      users.insert({'name': request.form['username'], 'password':hashpass})
      session['username'] = request.form['username']
      return redirect(url_for('index'))

    return 'Username already exists'
  return render_template('register.html')


  return ''



if __name__ == '__main__':
  app.secret_key = 'mysecret'
  app.run(debug=True)