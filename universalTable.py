#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
import MySQLdb
import getpass
import datetime

# connect
usr = raw_input("User: ")
passd = getpass.getpass()

db = MySQLdb.connect(host="localhost", user=usr, passwd=passd, db="conferencescheduler")

def addResource():
    global usr
    name = raw_input("Resource name: ")
    description = raw_input("Description: ")
    typeID = raw_input("ID of resource type: ")
    parent = raw_input("Enter parent ID (if applicable): ")
    userID = getIDFromName(usr)
    updateDate = datetime.datetime.now()
    try:
        int(typeID)
        parent = int(parent) if parent else "NULL"
        int(userID)
    except:
        print "Error! invalid data dype used"
        return
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO resources
            (name,
            description,
            type_id,
            last_updated_by,
            parent_resource_id)
        VALUES (\"{}\",\"{}\",{},{},{})
        """.format(
            name,
            description,
            typeID,
            userID,
            #updateDate,
            parent)
        )

def getIDFromName(name):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name = \"{}\"".format(name))
    result = cursor.fetchall()
    if result: return result[0]
    return "0"

def addUser():
    global usr
    fName = raw_input("First name: ")
    mName = raw_input("Middle name: ")
    lName = raw_input("Last name: ")
    role_id = raw_input("Role ID: ")
    email = raw_input("Email: ")
    phone = raw_input("Phone: ")
    lastUser = getIDFromName(usr)
    updateDate = datetime.datetime.now()
    try:
        int(role_id)
    except:
        print "Error! invalid data dype used"
        return
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO users
            (first_name,
            mid_name,
            last_name,
            role_id,
            mail,
            phone,
            last_updated_by,
            last_updated_date
            VALUES (\"{}\",\"{}\",\"{}\",{},\"{}\",\"{}\",{},{})
        """.format(
            fName,
            mName,
            lName,
            role_id,
            email,
            phone,
            lastUser,
            updateDate)
        )
    
while True:
    choice = raw_input("\nChoose:" +
                       "\n0) Commit changes" +
                       "\n1) Add resource" +
                       "\n2) Add user" +
                       "\n")
    if choice == "0": db.commit()
    elif choice == "1": addResource()
    elif choice == "2": addUser()
    print "\n"
"""
    # create a cursor
    cursor = db.cursor()

    # execute SQL statement
    cursor.execute("SELECT * FROM resources")

    # get the resultset as a tuple
    result = cursor.fetchall()

    # iterate through resultset
    for record in result:
        print record
        #print record[0] , "–>", record[1]
    db.commit()
"""
