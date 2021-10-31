from flask import Flask, redirect, render_template, url_for, request, session
from pymongo import MongoClient
import bcrypt
from datetime import date

application = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)

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

@application.route("/login/", methods = ["POST", "GET"])
def login():
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    # Problem exists here, method 1 = 'method' object is not scriptable
    login_user = users.find_one({'name': request.form.get('username')})

    #if login_user is None:
    #    return redirect(url_for('register'))
    # method 2, The browser (or proxy) sent a request that this server could not understand. KeyError: 'username'
    #login_user = users.find_one({'name': request.form['username']})

    user_pass = login_user['password']
    login_pass = request.form.get('password')


    # Method 1
    if bcrypt.checkpw(login_pass.encode('utf-8'), user_pass):
       return 'Test successful'
    else:
        return 'Test Failed'

    # Method 2
    
    """if login_user:
        if bcrypt.hashpw(request.form.get('password').encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            return redirect(url_for(landingPage))
        return 'Invalid'
    return 'Invalid'"""


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