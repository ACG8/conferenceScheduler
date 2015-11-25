from functions import *
from flask import Flask, render_template, request, session
from email.mime.text import MIMEText
from subprocess import Popen, PIPE
app = Flask(__name__)
app.secret_key = "fdfiwdf8qfy82hcuiqch82ht2ghwrfqrjvb8rvg924f4ygheufqeu2g72hg24hfefw4g24"

#currentUser = ""
#date = ""

# Index page. Presents the sign in form when first presented.
@app.route("/")
def main():
	#Should clear session here TODO
	return render_template("index.html")	


# Login function: Checks if the person logs in successfully, if they do show the hello page for now, else stay on login page
@app.route("/login", methods=['POST'])
def login():
	data = request.form
	print data
	if checkSignIn(data['username'], data['password']):
		session["username"] = data['username']
		return render_template("dashboard.html")
	else:
		return render_template("index.html")
		
@app.route("/forgotpassword")
def forgot_password():
	return render_template("forgotpassword.html")
	
@app.route("/forgot", methods=['POST'])
def forgot():
	data = request.form
	info = getPasswordAndEmail(data['username'])
	
	msg = MIMEText("Your password is " + info[0])
	msg["From"] = "conference@forgot.com"
	msg["To"] = info[1]
	msg["Subject"] = "Forgot Password"
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	p.communicate(msg.as_string()) 
	
	return render_template("index.html")

# Signup page: Simply shows the signup page.
@app.route("/signuppage")
def sign_up_page():
	return render_template("signup.html")

@app.route("/dashboardpage")
def dashboard_page():
	return render_template("dashboard.html")

@app.route("/preferencespage")
def preferences_page():
	return render_template("preferences.html")

@app.route("/reservationspage")
def reservations_page():
	return render_template("reservations.html", reservations = getReservations(session["username"]))
	
@app.route("/reserve")
def reserve_page():
	return render_template('reservepage.html')

@app.route("/searchpage")
def search_page():
	res = getResourceTypes()
	return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings())

@app.route("/changePassword", methods=['POST'])
def change_password():
	data = request.form
	if data["newpass"] and data["newpass"] == data["renewpass"]:
		changePassword(session["username"],data["newpass"])
	return render_template("preferences.html")

@app.route("/search", methods=['POST'])
def search():
	data = request.form
	session['date'] = data['date']
	resourceTypeIDs = getResourceTypes()
	filterResources = [rType[0] for rType in resourceTypeIDs if data.get("rescType " + str(rType[0]))]
	rooms = filterLocations(data['building'])
	rooms = [room for room in rooms if checkHasResources(room[1],filterResources)]
	if session["date"]: return render_template("rooms.html", building = (getBuildingName(data["building"]),data["building"]), rooms = rooms)
	return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings(), notification = "Must select a date")

# Signup function: Gets result from account creation and if successful shows the hello page with data, else shows the signup page with error
@app.route("/signup", methods=['POST'])
def sign_up():
	data = request.form
	account = createAccount(data['username'],data['password'],data['passwordconfirmation'],data['firstname'],data['lastname'],data['email'])
	print account
	if account[0]:
		session["username"] = data['username']
		return render_template("dashboard.html")
	else:
		return render_template("signup.html", data = account[1])
		
@app.route("/rooms/<resourceid>")
def rooms(resourceid):
	session['rid'] = resourceid
	children = getChildResources(resourceid,"type_id")
	children = [getResourceName(r) for r in children]
	rscText = getResourceLocation(resourceid)
	rscText = (getBuildingName(rscText[0]), rscText[1])
	reservations = getReservationFromDate(session['date'])
	items = []
	for item in reservations:
		if int(item[1]) == int(resourceid):
			items.append(str(item[2].time().hour) + ":" + str(item[2].time().minute) + " - " + str(item[3].time().hour) + ":" + str(item[3].time().minute))
	return render_template("resource.html", resourcetext = rscText, resource = resourceid , children = children, reservations = reservations, date = session['date'], items = items)

@app.route("/rooms/reserve", methods=['POST'])
def reserve():
	data = request.form
	if data['starttime'] >= data['endtime']:
		return render_template("reservations.html", reservations = getReservations(session["username"]), notification = "Error - start time must be before end time")
	start = str(session['date']) + ' ' + str(data['starttime'] + ':00')
	end = str(session['date']) + ' ' + str(data['endtime'] + ':00')
	currentuser = session['username']
	resourceid = session['rid']
	makeReservation(currentuser,resourceid,start,end)
	return render_template("reservations.html", reservations = getReservations(session["username"]))

@app.route("/reservations/<reservationid>")
def unreserve(reservationid):
	deleteReservation(reservationid)
	return render_template("reservations.html", reservations = getReservations(session["username"]))

if __name__ == "__main__":
	app.run()
	
