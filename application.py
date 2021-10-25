from flask import Flask, redirect, render_template, url_for, request, session
from pymongo import MongoClient
import bcrypt
from datetime import date

application = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)



@application.route("/login/", methods = ["POST", "GET"])
def login():
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    login_user = users.find_one({'name': request.form['username']})
    user_pass = login_user['password']

    if login_user and bcrypt.checkpw(request.form['password'], user_pass):
        print("Test successful")
    else:
        print("Test Failed")

@application.route('/register/', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'date': str(date.today()),'name': request.form['username'], 'password':hashpass, 'email': request.form['email'], 'phonenumber': request.form['phonenumber'], 'labor':request.form['keywords']})
            #session['username'] = request.form['username']
            return redirect(url_for('landingPage'))

        return 'Username already exists'
    return render_template('register.html')

@application.route("/results/")
def resultsPage():
	return render_template("resultsPage.html")

@application.route("/")
def landingPage():
	return render_template("landingPage.html")

@application.route("/<usr>/")
def user(usr):
	return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    application.run(debug=True)