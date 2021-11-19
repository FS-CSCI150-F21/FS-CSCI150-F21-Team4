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
import base64
import requests
from twitterScrapeV1 import getValid

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

application = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)

twitterAppToken = {
    "oauth_token" : "",
    "oauth_token_secret" : "",
    "oauth_verifier" : ""
}

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
            consumer_key = "uaC0BoALYt6SzxdNiWoOpvGym"
            consumer_secret = "NHc7uMZLM3zk77fZ7EuOzqSfuDnpqN52ZsTiLGh2k5CylsEPpj"
            access_token_url = 'https://api.twitter.com/oauth/access_token'
            consumer = oauth.Consumer(consumer_key, consumer_secret)
            client = oauth.Client(consumer)

            token = oauth.Token(twitterAppToken['oauth_token'], twitterAppToken['oauth_token_secret'])
            token.set_verifier(oauth_verifier)
            client = oauth.Client(consumer, token)

            resp, content = client.request(access_token_url, "POST")
            access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

            dashFound = False
            newToken = ""
            currentToken = access_token['oauth_token']
            for i in range(len(currentToken)):
                curChar = currentToken[i]
                if curChar == '-':
                    dashFound = True
                elif dashFound is True:
                    newToken = newToken + curChar
            print(f"Formatted token is: {newToken}")
            access_token['oauth_token'] = newToken

            print ("Access Token:")
            print ("    - oauth_token        = {}".format(access_token['oauth_token']))
            print ("    - oauth_token_secret = {}".format(access_token['oauth_token_secret']))

            print ("You may now access protected resources using the access tokens above.")
            consumer_key = access_token['oauth_token']
            consumer_secret = access_token['oauth_token_secret']

            #------------------- secret key generation----------------
            key_secret = f'{consumer_key}:{consumer_secret}'.encode('ascii')

            b64_encoded_key = base64.b64encode(key_secret)
            b64_encoded_key = b64_encoded_key.decode('ascii')
            base_url = 'https://api.twitter.com/'
            auth_url = '{}oauth2/token'.format(base_url)

            auth_headers = {
                'Authorization': 'Basic {}'.format(b64_encoded_key),
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }

            auth_data = {
                'grant_type': 'client_credentials'
            }

            auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
            if getValid(auth_resp) == False:
                return [], False
            access_token = auth_resp.json()['access_token']

            #------------------- Start of Mention Finder--------------
            ##Create HTTP headers
            search_headers = {
                'Authorization': 'Bearer {}'.format(access_token)    
            }
            response = requests.get(url = 'https://api.twitter.com/1.1/account/verify_credentials.json' , headers=search_headers)
            print(response.status_code)
            credVerify = response.json()
            print(credVerify)
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

    callbackURL = 'http://127.0.0.1:5000/'
    request_token_url = f'https://api.twitter.com/oauth/request_token?oauth_callback={callbackURL}'
    authenticate_url = 'https://api.twitter.com/oauth/authenticate'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    twitterAppToken['oauth_token'] = request_token['oauth_token']
    twitterAppToken['oauth_token_secret'] = request_token['oauth_token_secret']

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