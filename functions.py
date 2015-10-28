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

def filterLocations(building,date,room=None):
    "Returns a set of tuples that match the filters: (room id, room name)"
    #Sanitize inputs
    building = sanitize(building)
    room = sanitize(room) if room else None

    attributes = ["abbv"] + (["room"] if room else [])
    operators = ["=" for a in attributes]
    values = [building] + ([room] if room else [])

    db = Connection("root","password","scheduler")
    dbTuple = db.select("tbl_room_locations",["room","name"],attributes,operators,values)
    print dbTuple


#SQL commands for testing

#Need to provide value for role id before can test; use the following:
#   insert into tbl_roles values (0,"user","a normal user","user");

#createAccount("alex","password","password","alex","hanson","hanson.alex@yahoo.com")
