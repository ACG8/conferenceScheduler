from functions import *
from flask import Flask, render_template, request
app = Flask(__name__)


# Index page. Presents the sign in form when first presented.
@app.route("/")
def main():
	return render_template("index.html")	


# Login function: Checks if the person logs in successfully, if they do show the hello page for now, else stay on login page
@app.route("/login", methods=['POST'])
def login():
	data = request.form
	if checkSignIn(data['username'], data['password']):
		return render_template("hello.html", data = data)
	else:
		return render_template("index.html")
	
	
# Signup page: Simply shows the signup page.
@app.route("/signuppage")
def sign_up_page():
	return render_template("signup.html")


# Signup function: Gets result from account creation and if successful shows the hello page with data, else shows the signup page with error
@app.route("/signup", methods=['POST'])
def sign_up():
	data = request.form
	account = createAccount(data['username'],data['password'],data['passwordconfirmation'],data['firstname'],data['lastname'],data['email'])
	if account[0]:
		return render_template("hello.html", data = data)
	else:
		return render_template("signup.html", data = account[1])
	
if __name__ == "__main__":
	app.run()
