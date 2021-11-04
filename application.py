from flask import Flask, redirect, render_template, url_for, request
from pymongo import MongoClient
import bcrypt
from datetime import date
from testData import rslts

application = Flask(__name__)

url = 'mongodb+srv://Admin:1234@wordofmouth.yoff3.mongodb.net/userRegistration?retryWrites=true&w=majority'
client = MongoClient(url)


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

@application.route("/login/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form['uname']
        psw = request.form['psw']
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")

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

@application.route("/results/")
def resultsPage():
	return render_template("resultsPage.html",rslts = rslts)

@application.route("/")
def landingPage():
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


if __name__ == "__main__":
    application.run(debug=True)

