from functions import *
from flask import Flask, render_template, request, session
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
	date = data['date']
	resourceTypeIDs = getResourceTypes()
	filterResources = [rType[0] for rType in resourceTypeIDs if data.get("rescType "+str(rType[0]))]
	rooms = filterLocations(data['building'])
	print rooms
	rooms = [room for room in rooms if checkHasResources(room[1],filterResources)]
	return render_template("rooms.html", building = (getBuildingName(data["building"]),data["building"]), rooms = rooms)
	"""
	else:
		rooms = filterLocations(data['building'], data['room'])
		print rooms
		return render_template("rooms.html", data = rooms)
	"""
# Signup function: Gets result from account creation and if successful shows the hello page with data, else shows the signup page with error
@app.route("/signup", methods=['POST'])
def sign_up():
	data = request.form
	account = createAccount(data['username'],data['password'],data['passwordconfirmation'],data['firstname'],data['lastname'],data['email'])
	if account[0]:
		session["username"] = data['username']
		return render_template("dashboard.html")
	else:
		return render_template("signup.html", data = account[1])
		
@app.route("/rooms/<resourceid>")
def rooms(resourceid):
	children = getChildResources(resourceid,"type_id")
	children = [getResourceName(r) for r in children]
	rscText = getResourceLocation(resourceid)
	rscText = (getBuildingName(rscText[0]), rscText[1])
	return render_template("resource.html", resourcetext = rscText, resource = resourceid , children = children)
	
if __name__ == "__main__":
	app.run()
