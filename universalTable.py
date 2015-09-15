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
    userID = getUserId(usr)
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

def getUserId(username):
    return "1"
    
while True:
    addResource()

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
    raw_input("")
