#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
from toolbox import *
import getpass
import datetime

def checkSignIn(username,password):
    """Checks username and password against database.
    returns bool for validity."""
    #Sanitize inputs
    username = sanitize(username)
    password = sanitize(password)

    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["password"],["username"],["="],[username])
    try: return dbTuple[0][0] == password
    except IndexError: return False

def getRoleId(username):
    db = Connection("root","password","scheduler")
    roleid = db.select("tbl_users",["role_id"],["username"],["="],[username])
    return roleid[0][0]

def createAccount(username,password,repass,fname,lname,email):
    """Attempts to create a new account with given info.
    Returns (bool,string) for success (with string indicating reason for failure"""
    #Sanitize inputs
    username = sanitize(username)
    password = sanitize(password)
    repass = sanitize(repass)
    fname = sanitize(fname)
    lname = sanitize(lname)
    email = sanitize(email)
    print "createaccount a"
    #Check whether password and repassword match
    if password != repass: return (False,"Failure - the given passwords do not match.")

    #Connect to database
    db = Connection("root","password","scheduler")
    
    #Check whether somebody already has that username
    dbTuple = db.select("tbl_users",["username"],["username"],["="],[username])
    if dbTuple: return (False,"Failure - username is taken.")

    #Format inputs with quotes
    username = "\"{}\"".format(username)
    password = "\"{}\"".format(password)
    repass = "\"{}\"".format(repass)
    fname = "\"{}\"".format(fname)
    lname = "\"{}\"".format(lname)
    email = "\"{}\"".format(email)
    print "createaccount b"
    #Establish account and return True
    print "createaccount c"
    date = "\"{}\"".format(str(datetime.datetime.now()))
    print "createaccount d"
    db.append("tbl_users",
              (username,password,fname,lname,email,
               date,"1"),
              ("username","password","first_name","last_name","mail",
               "last_updated_date","role_id"))
    print "createaccount e"
    db.commit()
    print "createaccount f"
    return (True, "Success - account created.")

def filterLocations(building,room=None):
    """Returns a set of tuples that match the filters."""
    #Sanitize inputs
    building = sanitize(building)
    room = sanitize(room) if room else None

    attributes = ["tbl_buildings_id"] + (["room"] if room else [])
    operators = ["=" for a in attributes]
    values = [building] + ([room] if room else [])

    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_room_locations",["room","tbl_resources_id"],attributes,operators,values)
    return dbTuple

def getReservationFromDate(date):
    """Returns a list of reservation ids beginning or ending on the specified date.
    Input must be in YYYY-MM-DD format"""
    date = sanitize(date)

    db = Connection("root","password","scheduler").db
    cursor = db.cursor()
    query = """
        SELECT * FROM tbl_reservations WHERE
        ( CAST(from_datetime AS DATE) = CAST('{}' AS DATE) )
        OR ( CAST(to_datetime AS DATE) = CAST('{}' AS DATE) );
    """.format(date,date)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def getReservationTimes(resourceID,date):
    """Gets a list of all intervals during which resource is reserved on date"""
    reservations = getReservationIDFromDate(date)
    reservationTimes = [(r[2],r[3]) for r in reservations if r[1]==resourceID]
    return reservationTimes

def getReservationFromID(id):
    """Returns a list of reservation ids beginning or ending on the specified date.
    Input must be in YYYY-MM-DD format"""
    id = sanitize(id)

    db = Connection("root","password","scheduler").db
    cursor = db.cursor()
    query = """
        SELECT * FROM tbl_reservations WHERE
        id = {};
    """.format(id)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def makeReservation(username,resourceID,start,end):
    db = Connection("root","password","scheduler")
    date = "\"{}\"".format(str(datetime.datetime.now()))
    db.append("tbl_reservations",
              ("{}".format(resourceID),"'{}'".format(start),"'{}'".format(end),"'{}'".format(username),"{}".format(date)),
              ("tbl_resources_id","from_datetime","to_datetime","reserved_by","reserved_date")
    )
    db.commit()

def getChildResources(resourceID,outputType):
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_resources",[outputType],["root_parent_resource_id"],["="],[resourceID])
    return [t[0] for t in dbTuple]

def getResourceName(resourceTypeID):
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_resc_type",["name"],["id"],["="],[resourceTypeID])
    print dbTuple[0][0]
    return dbTuple[0]

def getRoomResourceId(buildingID,roomID):
    "Takes the id of a room and returns the id of the associated resource"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_room_locations",["tbl_resources_id"],["tbl_buildings_id","room"],["=","="],[buildingID,roomID])
    return dbTuple

def changePassword(username,password):
    "Changes username's password"
    db = Connection("root","password","scheduler")
    db.update("tbl_users",["password"],[password],["username"],["="],[username])
    db.commit()

def getResourceTypes():
    "Returns a list of resource ids and types"
    db = Connection("root","password","scheduler")
    dbTuple = db.selectAll("tbl_resc_type",["id","name"])
    return dbTuple

def getBuildings():
    "Returns a list of buildings"
    db = Connection("root","password","scheduler")
    dbTuple = db.selectAll("tbl_buildings",["id","name"])
    return dbTuple

def getBuildingName(bId):
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_buildings",["name"],["id"],["="],[bId])
    return dbTuple[0][0]

def getFutureReservations(username):
    "Returns all future reservations for username"
    date = "{}".format(str(datetime.datetime.now()))
    db = Connection("root","password","scheduler")
    cursor = db.execute("select id,tbl_resources_id, from_datetime, to_datetime from tbl_reservations where reserved_by = \"{}\" and from_datetime > now()".format(username))
    return cursor.fetchall()

def getCurrentReservations(username):
    "Returns all current reservations for username"
    date = "{}".format(str(datetime.datetime.now()))
    db = Connection("root","password","scheduler")
    cursor = db.execute("select id,tbl_resources_id, from_datetime, to_datetime from tbl_reservations where reserved_by = \"{}\" and from_datetime <= now() and now() <= to_datetime".format(username))
    return cursor.fetchall()

def getPastReservations(username):
    "Returns all past reservations for username"
    date = "{}".format(str(datetime.datetime.now()))
    db = Connection("root","password","scheduler")
    cursor = db.execute("select id,tbl_resources_id, from_datetime, to_datetime from tbl_reservations where reserved_by = \"{}\" and to_datetime < now()".format(username))
    return cursor.fetchall()

def deleteReservation(Rid):
    db = Connection("root","password","scheduler")
    db.delete("tbl_reservations",["id"],["="],[Rid])
    db.commit()

def getResourceLocation(resourceID):
    "Returns the building,roomid of a resource (specifically, a room)"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_room_locations",["tbl_buildings_id","room"],["tbl_resources_id"],["="],[resourceID])
    return dbTuple[0]

def getPasswordAndEmail(username):
    "Returns username's password and email (in that order)"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["password","mail"],["username"],["="],[username])
    return dbTuple[0]

def getUserData(username):
    "Returns user data for user's profile view, annotated with name of attribute"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["username","first_name","last_name","mail"],["username"],["="],[username])
    roleid = getRoleId(username)
    dbTuple2 = db.select("tbl_roles",["name"],["id"],["="],[roleid])
    raw = [a for a in dbTuple[0]] + [dbTuple2[0][0]]
    print raw
    basicData = [
        ("Username",raw[0]),
        ("Name","{} {}".format(raw[1],raw[2])),
        ("Email",raw[3]),
        ("User Type",raw[4])
        ]
    print basicData
    return basicData

def checkHasResources(roomID,rscTypeIDList):
    "Checks whether a roomid has all resources listed."
    resourceTypes = getChildResources(roomID,"type_id")
    print "a"
    print resourceTypes
    print "b"
    for rscT in rscTypeIDList:
        if not rscT in resourceTypes:
            return False
    return True

############################################################
################    Management Functions    ################
############################################################

def getNewUsers():
    "Returns a list of new users"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["username"],["role_id"],["="],[1])
    return [d[0] for d in dbTuple]

def getNewAndRegUsers():
    "Returns a list of new and regular users"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["username"],["role_id"],["<"],[3])
    return [d[0] for d in dbTuple]

def getManagers():
    "Returns a list of managers"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["username"],["role_id"],["="],[3])
    return [d[0] for d in dbTuple]

def getMyUsers(username):
    "Returns a list of users whose manager is the current user"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_users",["username"],["manager"],["="],[username])
    return [d[0] for d in dbTuple]

def changeManager(username,newManager):
    "Changes a user's manager"
    db = Connection("root","password","scheduler")
    db.update("tbl_users",["manager"],[newManager],["username"],["="],[username])
    db.commit()

def changeUserRole(username,newRoleId):
    "Changes a user's role"
    db = Connection("root","password","scheduler")
    db.update("tbl_users",["role_id"],[newRoleId],["username"],["="],[username])
    db.commit()

def getRoles():
    "Returns all roles"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_roles",["name","id"],["id"],[">"],[0])
    return dbTuple

def getFeedback(resourceID):
    "Returns all feedback for the given resource"
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_reviews",["rating", "comments", "created_on"],["tbl_resources_id"],["="],[resourceID])
    return dbTuple

def giveFeedback(resourceID,rating,comments):
    db = Connection("root","password","scheduler")
    date = "\"{}\"".format(str(datetime.datetime.now()))
    db.append("tbl_reviews",
              ("{}".format(resourceID),"{}".format(rating),"'{}'".format(comments),"{}".format(date)),
              ("tbl_resources_id","rating","comments","created_on")
    )
    db.commit()

