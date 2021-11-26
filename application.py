from flask import Flask, redirect, render_template, url_for, request, session, g, flash
from pymongo import MongoClient
import bcrypt
import pickle
import sklearn
from datetime import date
#from testData import rslts
#from profileLoadingTestData import profileResult
from flask_login import login_user
import certifi


from tweetSentiment import tweetSentimentAnalyzer, textSentimentAnalyzer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import urllib.request
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/profilePic'
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
application.secret_key = 'free3070herebozo'

client = MongoClient(url)
push = bool(True)

client = MongoClient(url, tlsCAFile=certifi.where())

@application.before_request
def before_request():
    g.user = None
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    if 'email' in session:
        user = users.find_one({'email': session['email']})
        g.user = user

@application.route("/login/", methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        session.pop('email', None)
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
        
        login_user = users.find_one({'name': request.form['username']})
        if login_user is None:
           return redirect(url_for('register'))

        user_pass = login_user['password']
        login_pass = request.form.get('password')

        # Method 1
        if bcrypt.checkpw(login_pass.encode('utf-8'), user_pass):
            login_email = login_user['email']
            session['email'] = login_email
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@application.route('/register/', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        if 'form-name' in request.form:
            usersDB = client["userRegistration"]
            users = usersDB['userregistrations']
            existing_user = users.find_one({'name': request.form['username']})

            if existing_user is None:
                hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                profile = {
                    "displayName": request.form['username'],
                    "labors": request.form['keywords'],
                    "location": "Fresno",
                    "imgLink": "",
                    "userBio": "Default Bio"
                }
                projects = [{
                    "projectName": "Estate Garden",
                    "projectDescription": " gabba gabbe",
                    "projImage1": "",
                    "projImage2": ""
                }]
                reviews = [{
                    "reviewerName": "Angry Guy",
                    "reviewScore": "4",
                    "reviewText": "yaddayadda",
                    "sentimentAnalysis": "Positive Review"
                }]

                users.insert_one({'date': str(date.today()),'name': request.form['username'], 'password':hashpass, 'email': request.form['email'], 'phonenumber': request.form['phonenumber'], 'labor':request.form['keywords'], 'profile':profile, 'projects':projects, 'reviews':reviews})
                #session['username'] = request.form['username']
                return redirect(url_for('landingPage'))

            return 'Username already exists'
        if 'login_form' in request.form:
            return login()
    return render_template('register.html')

@application.route("/logout/", methods=["POST", "GET"])
def logout():
    if request.method == 'POST':
        if 'login_form' in request.form:
            return login()
    if 'email' in session:
        session.pop('email', None)
        return render_template('logout.html')
    else:
        return redirect(url_for('landingPage'))

@application.route("/results/", methods = ['POST','GET'])
def resultsPage():
    if request.method == 'POST':
        if 'form-name' in request.form:
            usersDB = client["userRegistration"]
            users = usersDB['userregistrations']
            searchQuery = {'labor': request.form['search'], 'profile.location': request.form['locationBar']}
            searchQuery = {k:v for k,v in searchQuery.items() if v != ""}
            searchResults = users.find(searchQuery)
            searchResults = searchResults[:10]
            return render_template("resultsPage.html",rslts = searchResults)
        if 'login_form' in request.form:
            return login()
    else:
        return render_template("resultsPage.html")

@application.route("/", methods = ["POST", "GET"])
def landingPage():
    if request.method == 'POST':
        if login():
            return login()
    return render_template("landingPage.html")

@application.route("/<usr>/", methods = ["POST", "GET"])
def user(usr):
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    
    profile_user = users.find_one({'name': usr})
    if profile_user is None:
        # This profile does not exist
        return render_template("resultsPage.html")

    isUser = False
    if not(g.user == None):
        if (g.user['name'] == usr):
            isUser = True
    return render_template("profile.html", profileResult = profile_user, isUser = isUser)
    
@application.route("/profile/", methods = ["POST", "GET"])
def profile():
    if request.method == 'POST':
        if 'login_form' in request.form:
            return login()
    if not g.user:
        return redirect(url_for('login'))
    else:
        existing_user = g.user
        profile = existing_user.get('profile', 'User labors is Empty.')
        projects = existing_user.get('projects', 'User projects is Empty.')
        reviews = existing_user.get('reviews', 'User reviews is Empty.')
        profileResult = {
            "profile": profile,
            "projects": projects,
            "reviews": reviews
        }
        return render_template("profile.html", profileResult = profileResult, isUser = True)

@application.route("/reviews/<usr>", methods = ["POST", "GET"])
def reviews(usr):
    if request.method == 'POST':
        if 'login_form' in request.form:
            return login()
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    profile_user = users.find_one({'name': usr})

    if profile_user is None:
        # This profile does not exist
        return render_template("resultsPage.html")

    isUser = False
    if not(g.user == None):
        if (g.user['name'] == usr):
            isUser = True

    review_data = [users.find_one({'name': review['reviewerName']})['profile']['location'] for review in profile_user['reviews']]
    print(review_data)
    for i, loc in enumerate(review_data):
        profile_user['reviews'][i]['location'] = loc
    print(profile_user['reviews'])

    return render_template("reviews.html", profileResult = profile_user, isUser = isUser)

@application.route("/addreview/<usr>", methods = ["POST", "GET"])
def addReview(usr):
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    profile_user = users.find_one({'name': usr})

    if request.method == 'POST':
        if 'login_form' in request.form:
            return login()
        reviewName = g.user['name']
        reviewStars = request.form.getlist('star')
        reviewScore = int(reviewStars[0])
        reviewText = request.form.get('reviewArea')
        sentiment = ""
        if (textSentimentAnalyzer(reviewText)):
            sentiment = "Positive Review"
        else:
            sentiment = "Negative Review"

        reviewValues = { "$push": {
            'reviews' : {
                    'reviewerName': reviewName,
                    'reviewScore' : reviewScore,
                    'reviewText' : reviewText,
                    'sentimentAnalysis' : sentiment,
                }
            }
        }

        users.update_one(profile_user, reviewValues)
        return redirect(url_for('reviews', usr=profile_user['name']))

    review_user = g.user

    return render_template("addReview.html", profileResult=profile_user, reviewUser=review_user)
    
@application.route("/profileEdit/", methods = ["POST", "GET"])
def profileEdit():
    if request.method == "POST":
        if 'login_form' in request.form:
            return login()
        username = request.form.get('username')
         #request.form.get('password')
        email = request.form.get('email')
        labor = request.form.get('labor')
        phone = request.form.get('phone')
        location = request.form.get('location')
        description = request.form.get('description')
       

        existing_user = g.user 
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
        login_user = users.find_one(existing_user)

        file = request.files.get('file')
        filename = file.filename
     

        #validator?
        if username == '':
            username = users['name']
        elif email == '':
            email = users['email']
        elif phone == '':
            phone = users['phonenumber']
        elif labor == '':
            email = users['email']
        elif location == '':
            flash('eh you dont need a location')
        elif filename == '': #bug here
            flash('No image selected for uploading')
            return redirect(request.url)
        
            
 
        #form module?
        newvalues = { "$set": {
            'date': str(date.today()),
            'name': username,  
            'email': email, 
            'phonenumber': phone, 
            'labor':labor, 
            'profile':{
                'displayName': username,
                'labors': labor,
                'location': location,
                'imgLink': filename,
                'userBio': description
            }
            
            }
        }

       

        if push: #need a security boost to prevent injections of code check file extensions
           
            file.save(os.path.join('static\profilePic', filename))
            #print('upload_image filename: ' + filename)
    
            if existing_user is None:
                return redirect(url_for('registration'))

            else:
                
                users.update_many(existing_user, newvalues)
                return redirect(url_for('profile'))
        
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')#security protocol
            return redirect(request.url)    
    
    return render_template("profileEdit.html")#, image_file = image_file)

@application.route("/addproj/", methods = ["POST", "GET"])
def addproj():
    if request.method == 'POST':
        if 'login_form' in request.form:
            return login()
        project = request.form.get('project')
        projDescription = request.form.get('projDescription')
        projImage1 = request.files.get('projImage1')
        projImage2 = request.files.get('projImage2')
        filename1 = projImage1.filename
        filename2 = projImage2.filename

        existing_user = g.user 
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
        login_user = users.find_one(existing_user)

        projValues = { "$push": {
            'projects' : {
                    'projName': project,
                    'projDescription' : projDescription,
                    'projImage1' : filename1,
                    'projImage2' : filename2,
                }
            }
        }

        if push: #need a security boost to prevent injections of code check file extensions
            projImage1.save(os.path.join('static/projectPic', filename1))
            projImage2.save(os.path.join('static/projectPic', filename2))
            #print('upload_image filename: ' + filename)
    
            if existing_user is None:
                return redirect(url_for('registration'))
            else:
                users.update_many(existing_user, projValues)
                return redirect(url_for('profile'))
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')#security protocol
            return redirect(request.url)
    return render_template("addproj.html")    

@application.route("/NLP/", methods = ["POST", "GET"])
def NLP():
    if request.method == 'POST':
        if 'login_form' in request.form:
            return login()
        data = []
        totalTweets = 20
        username = request.form.get('Username')
        results, foundTweets  = tweetSentimentAnalyzer(userName=username, totalTweets=totalTweets)
        if foundTweets is False:
            return render_template("NLP.html", data = "")
        else:
            positiveTweets = results['tweet_postive']
            negativeTweets = results['tweet_negative']

            reviewValues = { "$set": {
            'Review' : { 
                'username' : username,   
                'positive' : positiveTweets,
                'negative' : negativeTweets,
                'totalTweets' : totalTweets,
                }
            }
        }

        if username is None:
            return redirect(url_for('NLP'))

        else:
            usersDB = client["userRegistration"]
            users = usersDB['userregistrations']
            users.update_many(username, reviewValues)
            return redirect(url_for('profile'))

    return render_template("NLP.html", data = "")

if __name__ == "__main__":
    application.run(debug=True)
