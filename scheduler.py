from flask import Flask, render_template, request
app = Flask(__name__)
from functions import *

@app.route("/")
def main():
	return render_template("index.html")	
	
@app.route("/login", methods=['POST'])
def login():
	data = request.form
	print data
	return render_template("hello.html", data = data)
	
@app.route("/signup/")
def sign_up():
	return render_template("signup.html")
	
if __name__ == "__main__":
	app.run()
