from flask import Flask, redirect, render_template, url_for, request

application = Flask(__name__)

@application.route("/login/", methods = ["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form['uname']
		psw = request.form['psw']
		return redirect(url_for("user", usr = user))
	else:
		return render_template("login.html")

@application.route("/register/")
def register():
	return render_template("register.html")

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