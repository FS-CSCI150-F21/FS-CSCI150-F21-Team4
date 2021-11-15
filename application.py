from flask import Flask, redirect, render_template, url_for, request, session
from pymongo import MongoClient
import bcrypt
import pickle
import sklearn
from datetime import date
from testData import rslts
from profileLoadingTestData import profileResult

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

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
    if request.method == 'POST':
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
       
        login_user = users.find_one({'name': request.form['username']})
        if login_user is None:
           return redirect(url_for('register'))

        user_pass = login_user['password']
        login_pass = request.form.get('password')


        # Method 1
        if bcrypt.checkpw(login_pass.encode('utf-8'), user_pass):
            return 'Test successful'
        else:
            return 'Test Failed'
    return render_template('login.html')


@application.route("/results/", methods = ['POST','GET'])
def resultsPage():
    if request.method == 'POST':
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
        searchResults = users.find({'labor': request.form['search']}) 

        return render_template("resultsPage.html",rslts = searchResults)
    else:
        return render_template("resultsPage.html")

@application.route("/", methods = ["POST", "GET"])
def landingPage():
    if request.method == 'POST':
        if login() == 'Test successful':
            return login()
    return render_template("landingPage.html")

@application.route("/<usr>/")
def user(usr):
	return f"<h1>{usr}</h1>"
    
@application.route("/profile/")
def profile():
    
    return render_template("profile.html", profileResult=profileResult )
    
@application.route("/profileEdit", methods = ["POST", "GET"])
def profileEdit():
    #imageFile = url_for('static', filname = 'profilePic/' + currentUser+image_file)
    return render_template("profileEdit.html")#, image_file = image_file)

@application.route("/NLP/", methods = ["POST", "GET"])
def NLP():
    if request.method == 'POST':
        filename = 'svm_model.sav'
        model = pickle.load(open(filename, 'rb'))
        text = request.form.get('NLPtext')
        prediction = model.predict([text])
        return render_template("NLP.html", data = [text, prediction[0]])
    return render_template("NLP.html", data = "")

if __name__ == "__main__":
    application.run(debug=True)