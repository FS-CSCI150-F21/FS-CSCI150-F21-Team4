from flask import Flask, redirect, render_template, url_for, request, session, g, flash
from pymongo import MongoClient
import bcrypt
import pickle
import sklearn
from datetime import date
from testData import rslts
from profileLoadingTestData import profileResult
from flask_login import login_user
import certifi


from tweetSentiment import tweetSentimentAnalyzer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import urllib.request
import os
from werkzeug.utils import secure_filename


application = Flask(__name__)

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
        if login():
            return login()
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
                "photoLink1": "../static/Images/testDataImages/projectImg1.jpg",
                "photoLink2": "../static/Images/testDataImages/projectImg2.jpg",
                "photoLink3": "../static/Images/testDataImages/projectImg3.jpg",
                "photoLink4": "../static/Images/testDataImages/projectImg4.jpg"
            }]
            reviews = [{
                "reviewerName": "Angry Guy",
                "reviewScore": "4",
                "reviewText": "yaddayadda",
                "??sentimentAnalysis": "Positive Review"
            }]

            users.insert_one({'date': str(date.today()),'name': request.form['username'], 'password':hashpass, 'email': request.form['email'], 'phonenumber': request.form['phonenumber'], 'labor':request.form['keywords'], 'profile':profile, 'projects':projects, 'reviews':reviews})
            #session['username'] = request.form['username']
            return redirect(url_for('landingPage'))

        return 'Username already exists'
    return render_template('register.html')

@application.route("/logout/", methods=["POST", "GET"])
def logout():
    if request.method == 'POST':
        if login():
            return login()
    if 'email' in session:
        session.pop('email', None)
        return render_template('logout.html')
    else:
        return redirect(url_for('landingPage'))

@application.route("/results/", methods = ['POST','GET'])
def resultsPage():
    if request.method == 'POST':
        #if login():
            #return login()
        usersDB = client["userRegistration"]
        users = usersDB['userregistrations']
        searchResults = users.find({'labor': request.form['search']}) 

        return render_template("resultsPage.html",rslts = searchResults)
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
        if login():
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
    
@application.route("/profileEdit/", methods = ["POST", "GET"])
def profileEdit():
    if request.method == "POST":
        if login():
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
        #if login():
            #return login()
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
            projImage1.save(os.path.join('static\projectPic', filename1))
            projImage2.save(os.path.join('static\projectPic', filename2))
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

@application.route("/landscaping", methods = ["GET"])
def grab():
    usersDB = client["userRegistration"]
    users = usersDB['userregistrations']
    searchResults = users.find({'labor': 'landscaping'}) 

@application.route("/NLP/", methods = ["POST", "GET"])
def NLP():
    if request.method == 'POST':
        if login():
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
