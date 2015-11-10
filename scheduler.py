from functions import *
from flask import Flask, render_template, request
app = Flask(__name__)


currentUser = ""
date = ""

# Index page. Presents the sign in form when first presented.
@app.route("/")
def main():
	return render_template("index.html")	


# Login function: Checks if the person logs in successfully, if they do show the hello page for now, else stay on login page
@app.route("/login", methods=['POST'])
def login():
	data = request.form
	print data
	if checkSignIn(data['username'], data['password']):
		currentUser = data['username']
		return render_template("search.html")
	else:
		return render_template("index.html")
	
	
# Signup page: Simply shows the signup page.
@app.route("/signuppage")
def sign_up_page():
	return render_template("signup.html")
	

@app.route("/search", methods=['POST'])
def search():
	data = request.form
	print data['building']
	date = data['date']
	if data['room'] == '':
		rooms = filterLocations(data['building'])
		print rooms
		return render_template("hello.html", data = rooms)
	else:
		rooms = filterLocations(data['building'], data['room'])
		print rooms
		return render_template("hello.html", data = rooms)


@app.route("/searchpage")
def search_page():
	return render_template("search.html")
	


# Signup function: Gets result from account creation and if successful shows the hello page with data, else shows the signup page with error
@app.route("/signup", methods=['POST'])
def sign_up():
	data = request.form
	account = createAccount(data['username'],data['password'],data['passwordconfirmation'],data['firstname'],data['lastname'],data['email'])
	if account[0]:
		currentUser = data['username']
		return render_template("search.html")
	else:
		return render_template("signup.html", data = account[1])
		
@app.route("/rooms")
def rooms():
        pass
	
	
if __name__ == "__main__":
	app.run()
