from flask import Flask, redirect, render_template, url_for, request, session
import flask
from pymongo import MongoClient
import bcrypt
import pickle
import sklearn
from datetime import date
from testData import rslts

import oauth2 as oauth
import urllib.parse

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

application = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)

twitterAppToken = {}

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@application.route('/register', methods = ['POST', 'GET'])
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
    if request.method == 'GET':
        oauth_verifier = request.args.get('oauth_verifier')
        if oauth_verifier is None:
            print("No oauth verifier")
        else:
            print("Found oauh verifier!")
        access_token_url = 'https://api.twitter.com/oauth/access_token'
    return render_template("landingPage.html")

@application.route("/<usr>/")
def user(usr):
	return f"<h1>{usr}</h1>"
    
@application.route("/profile/")
def profile():
    return render_template("profile.html")
    
@application.route("/profileEdit")
def profileEdit():
    #imageFile = url_for('static', filname = 'profilePic/' + currentUser+image_file)
    return render_template("profileEdit.html")#, image_file = image_file)

@application.route("/NLP/", methods = ["POST", "GET"])
def NLP():
    consumer_key = "uaC0BoALYt6SzxdNiWoOpvGym"
    consumer_secret = "NHc7uMZLM3zk77fZ7EuOzqSfuDnpqN52ZsTiLGh2k5CylsEPpj"

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    authenticate_url = 'https://api.twitter.com/oauth/authenticate'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    print ("Request Token:")
    print ("    - oauth_token        = {}".format(request_token['oauth_token']))
    print ("    - oauth_token_secret = {}".format(request_token['oauth_token_secret'])) 
    redirectURL = "{0}?oauth_token={1}".format(authenticate_url, request_token['oauth_token'])
    return flask.redirect(redirectURL, code=302)    

    if request.method == 'POST':
        filename = 'svm_model.sav'
        model = pickle.load(open(filename, 'rb'))
        text = request.form.get('NLPtext')
        prediction = model.predict([text])
        return render_template("NLP.html", data = [text, prediction[0]])
    return render_template("NLP.html", data = "")

if __name__ == "__main__":
    application.run(debug=True)