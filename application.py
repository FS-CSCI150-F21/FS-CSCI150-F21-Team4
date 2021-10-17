from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)

@app.route("/login", methods = ["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form['uname']
		psw = request.form['psw']
		return redirect(url_for("user", usr = user))
	else:
		return render_template("login.html")

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/results")
def resultsPage():
	return render_template("resultsPage.html")

@app.route("/")
def landingPage():
	return render_template("landingPage.html")

@app.route("/<usr>")
def user(usr):
	return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)