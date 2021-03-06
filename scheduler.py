from functions import *
from flask import Flask, render_template, request, session
#from flask_mail import Mail, Message
import datetime
app = Flask(__name__)
#mail = Mail(app)
app.secret_key = "fdfiwdf8qfy82hcuiqch82ht2ghwrfqrjvb8rvg924f4ygheufqeu2g72hg24hfefw4g24"

#currentUser = ""
#date = ""




############################################################
################    Navigation Functions    ################
############################################################

# Index page. Presents the sign in form when first presented.
@app.route("/")
def main():
	#Should clear session here TODO
	return render_template("index.html")

@app.route("/forgotpassword")
def forgot_password():
	return render_template("forgotpassword.html")

# Signup page: Simply shows the signup page.
@app.route("/signuppage")
def sign_up_page():
	return render_template("signup.html")

@app.route("/dashboardpage")
def dashboard_page():
	return render_template("dashboard.html", privilege = session["role id"])

@app.route("/preferencespage")
def preferences_page():
	data = getUserData(session["username"])
	return render_template("preferences.html", data = data, privilege = session["role id"])

@app.route("/reservationspage")
def reservations_page():
	return render_template(
		"reservations.html", 
		FutureReservations = getFutureReservations(session["username"]),
		CurrentReservations = getCurrentReservations(session["username"]),
		PastReservations = getPastReservations(session["username"]),
		privilege = session["role id"])

@app.route("/searchpage")
def search_page():
	return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings(), privilege = session["role id"])

@app.route("/managementpage")
def management_page():
	if session["role id"] > 3:
		users = getRegUsers() + getManagers()
	else:
		users = getMyUsers(session["username"])
	return render_template("management.html", newUsers = getNewUsers(), myUsers = users, privilege = session["role id"])

@app.route("/report")
def report_page():
	return render_template("report.html", privilege = session["role id"])
	print "Open report page"

@app.route("/adminpage")
def admin_page():
	return render_template("admin.html", users = getNewAndRegUsers(), privilege = session["role id"])

############################################################
################      Account Functions     ################
############################################################

# Login function: Checks if the person logs in successfully, if they do show the hello page for now, else stay on login page
@app.route("/login", methods=['POST'])
def login():
	data = request.form
	username = data["username"]
	if checkSignIn(username, data['password']):
		session["username"] = username
		session["role id"] = getRoleId(username)
		return dashboard_page()
	else:
		return render_template("index.html")
		
@app.route("/forgot", methods=['POST'])
def forgot():
	data = request.form
	info = getPasswordAndEmail(data['username'])
	
	#msg = Message("Your password is " + str(info[0]),
					#sender="conference@forgot.com",
					#recipients=[info[1]])
	print "setup message"
	#mail.send(msg)
	print "message sent"
	return render_template("index.html")

# Signup function: Gets result from account creation and if successful shows the hello page with data, else shows the signup page with error
@app.route("/signup", methods=['POST'])
def sign_up():
	print "signup a"
	data = request.form
	print "signup b"
	account = createAccount(data['username'],data['password'],data['passwordconfirmation'],data['firstname'],data['lastname'],data['email'])
	print "signup c"
	print account
	print "signup d"
	if account[0]:
		print "signup e"
		session["username"] = data['username']
		print "signup f"
		return render_template("index.html")
	else:
		return render_template("signup.html", data = account[1])

@app.route("/changePassword", methods=['POST'])
def change_password():
	data = request.form
	if data["newpass"] and data["newpass"] == data["renewpass"]:
		changePassword(session["username"],data["newpass"])
	return render_template("preferences.html")

############################################################
################   Reservation Functions    ################
############################################################

@app.route("/search", methods=['POST'])
def search():
	data = request.form
	session["date"] = data["date"]
	if not session["date"]: 
		return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings(), notification = "Must select a date.", privilege = session["role id"])
	date = datetime.datetime.strptime(session["date"],"%Y-%m-%d").date()
	resourceTypeIDs = getResourceTypes()
	filterResources = [rType[0] for rType in resourceTypeIDs if data.get("rescType " + str(rType[0]))]
	rooms = filterLocations(data['building'])
	rooms = [room for room in rooms if checkHasResources(room[1],filterResources)]
	print datetime.datetime.now().date()
	if date < datetime.datetime.now().date():
		return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings(), notification = "Cannot select a date in the past.", privilege = session["role id"])
	return render_template("rooms.html", building = (getBuildingName(data["building"]),data["building"]), rooms = rooms, privilege = session["role id"])
	
		
@app.route("/rooms/<resourceid>")
def rooms(resourceid):
	session['rid'] = resourceid
	children = getChildResources(resourceid,"type_id")
	children = [getResourceName(r) for r in children]
	rscText = getResourceLocation(resourceid)
	rscText = (getBuildingName(rscText[0]), rscText[1])
	feedback = getFeedback(resourceid)
	reservations = getReservationFromDate(session["date"])
	items = []
	for item in reservations:
		if int(item[1]) == int(resourceid):
			items.append("{} - {}".format(str(item[2].strftime("%I:%M %p")),str(item[3].strftime("%I:%M %p"))))
	return render_template("resource.html", resourcetext = rscText, resourceid = resourceid , children = children, reservations = reservations, date = session["date"], items = items, feedback = feedback, privilege = session["role id"])

@app.route("/rooms/reserve", methods=['POST'])
def reserve():
	data = request.form
	starttime = datetime.datetime.strptime(data['starttime'],"%H:%M").time()
	endtime = datetime.datetime.strptime(data['endtime'],"%H:%M").time()
	date = datetime.datetime.strptime(session["date"],"%Y-%m-%d").date()
	now = datetime.datetime.now()
	if (date <= now.date() and starttime < now.time()) or starttime >= endtime:
		return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings(), notification = "Cannot select a time in the past.", privilege = session["role id"])
	start = "{} {}:00".format(session["date"],data["starttime"])
	end = "{} {}:00".format(session["date"],data["endtime"])
	currentuser = session['username']
	resourceid = session['rid']
	count = int(data['Amount'])
	if count == 0:
		makeReservation(currentuser,resourceid,start,end)
	else:
		count = int(data['Amount'])
		over = 0
		while count > -1:
			makeReservation(currentuser,resourceid,start,end)
			month = int(session["date"][5:7]) + count
			if month > 12:
				month = '0' + str(1 + over)
				print month
				year = int(session["date"][:4]) + 1
				day = int(session["date"][-2:])
				over = over + 1
			else:
				day = int(session["date"][-2:])
				year = int(session["date"][:4])
			start = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(data['starttime'] + ':00')
			end = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(data['endtime'] + ':00')
			count = count - 1
	return reservations_page()
	
@app.route("/feedback/feedback", methods=['POST'])
def feedback():
	data = request.form
	resourceid = data['resourceid']
	rating = data['rating']
	comment = data['comment']
	giveFeedback(resourceid,rating,comment)
	return dashboard_page()

@app.route("/reservations/<reservationid>")
def unreserve(reservationid):
	deleteReservation(reservationid)
	return reservations_page()

@app.route("/reportresult", methods=['POST'])
def query():
	print "Executing query"
	return render_template("reportresult.html", report = getReport(request.form["fromDate"], request.form["toDate"]), privilege = session["role id"])



@app.route("/feedback/<resourceid>")
def feedback_resource(resourceid):
	return render_template("feedback.html",resourceid = resourceid)
############################################################
################    Management Functions    ################
############################################################

@app.route("/manage/claim/<username>")
def claim(username):
	me = session["username"]
	changeManager(username,me)
	changeUserRole(username,2) #Make them into normal users
	return management_page()
	
@app.route("/manage/reservations/<username>")
def managerRes(username):
	return render_template(
			"manageReservations.html", 
			FutureReservations = getFutureReservations(username),
			CurrentReservations = getCurrentReservations(username),
			PastReservations = getPastReservations(username),
			privilege = session["role id"])
			
@app.route("/manage/update/<reservationid>")
def managerUpd(reservationid):
	reservation = getReservationFromID(reservationid)
	children = getChildResources(reservation[0][1],"type_id")
	children = [getResourceName(r) for r in children]
	rscText = getResourceLocation(reservation[0][1])
	rscText = (getBuildingName(rscText[0]), rscText[1])
	feedback = getFeedback(reservation[0][1])
	reservations = getReservationFromDate(session["date"])
	items = []
	for item in reservations:
		if int(item[1]) == int(resourceid):
			items.append("{} - {}".format(str(item[2].strftime("%I:%M %p")),str(item[3].strftime("%I:%M %p"))))
	return render_template("manageUpdate.html", resourcetext = rscText, resourceid = reservation[0][1] , children = children, reservations = reservations, date = reservation[0][2].date(), items = items, feedback = feedback, privilege = session["role id"], resFromTime = reservation[0][2].time(), resToTime = reservation[0][3].time(), reservationid = reservationid)
	
@app.route("/manage/update/update", methods=['POST'])
def manageResUpdate():
	data = request.form
	starttime = datetime.datetime.strptime(data['starttime'],"%H:%M").time()
	endtime = datetime.datetime.strptime(data['endtime'],"%H:%M").time()
	date = datetime.datetime.strptime(session["date"],"%Y-%m-%d").date()
	now = datetime.datetime.now()
	if (date >= now.date() and starttime < now.time()) or starttime >= endtime:
		return render_template("search.html", resourceTypes = getResourceTypes(), buildings = getBuildings(), notification = "Cannot select a time in the past.", privilege = session["role id"])
	start = "{} {}:00".format(session["date"],data["starttime"])
	end = "{} {}:00".format(session["date"],data["endtime"])
	currentuser = session['username']
	resourceid = data['resourceid']
	count = int(data['Amount'])
	if count == 0:
		makeReservation(currentuser,data['resourceid'],start,end)
	else:
		count = int(data['Amount'])
		over = 0
		while count > -1:
			makeReservation(currentuser,data['resourceid'],start,end)
			month = int(session["date"][5:7]) + count
			if month > 12:
				month = '0' + str(1 + over)
				print month
				year = int(session["date"][:4]) + 1
				day = int(session["date"][-2:])
				over = over + 1
			else:
				day = int(session["date"][-2:])
				year = int(session["date"][:4])
			start = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(data['starttime'] + ':00')
			end = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(data['endtime'] + ':00')
			count = count - 1
	deleteReservation(data['reservationid'])
	return managementPage()
	


############################################################
################       Admin Functions      ################
############################################################	
@app.route("/admin/change")
def admin_change():
	return render_template("adminChange.html", users = getNewAndRegUsers(), managers = getManagers() + getAdmins(), privilege = session["role id"])
	
@app.route("/admin/changeManager", methods=['POST'])
def admin_changeManager():	
	data = request.form
	changeManager(data['username'],data['manager'])
	return admin_page()

@app.route("/admin/role")
def admin_role():
	return render_template("adminRole.html", users = getNewAndRegUsers() + getManagers(), roles = getRoles(), privilege = session["role id"])

@app.route("/admin/changeRole", methods=['POST'])
def admin_changeRole():		
	data = request.form
	print data
	changeUserRole(data['username'],data['role'])
	return admin_page()


############################################################
################            Main            ################
############################################################
if __name__ == "__main__":
	app.run()