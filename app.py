from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/register")
def register():
	return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)