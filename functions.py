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

    #Establish account and return True
    date = "\"{}\"".format(str(datetime.datetime.now()))
    db.append("tbl_users",
              (username,password,fname,lname,email,
               username,date,"0"),
              ("username","password","first_name","last_name","mail",
               "last_updated_by","last_updated_date","role_id"))
    db.commit()
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

def makeReservation(username,resourceID,start,end):
    db = Connection("root","password","scheduler")
    datetime = "\"{}\"".format(str(datetime.datetime.now()))
    db.append("tbl_reservations",
              ("'{}'".format(resourceID),"'{}'".format(start),"'{}'".format(end),"'{}'".format(user),"'{}'".format(datetime)),
              ("tbl_resources_id","from_datetime","to_datetime","reserved_by","reserved_date")
    )
    db.commit()


def getChildResources(resourceID):
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_resources",["id"],["root_parent_resource_id"],["="],[resourceID])
    return dbTuple

def getResourceName(resourceTypeID):
    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_resc_type",["name"],["id"],["="],[resourceTypeID])
    print dbTuple[0][0]

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

#2015-10-28
#SQL commands for testing

#Need to provide value for role id before can test; use the following:
#   insert into tbl_roles values (0,"user","a normal user","user");

#createAccount("alex","password","password","alex","hanson","hanson.alex@yahoo.com")
