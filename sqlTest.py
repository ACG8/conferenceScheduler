#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
import MySQLdb
import getpass

# connect
usr = raw_input("User: ")
passd = getpass.getpass()

db = MySQLdb.connect(host="localhost", user=usr, passwd=passd, db="menagerie")

def showTables():
    db = MySQLdb.connect(host="localhost", user=usr, passwd=passd, db="menagerie")

def listTable():
    cursor = db.cursor()
    

while True:

    # create a cursor
    cursor = db.cursor()

    # execute SQL statement
    cursor.execute("SELECT * FROM pet")

    # get the resultset as a tuple
    result = cursor.fetchall()

    # iterate through resultset
    for record in result:
        print record
        #print record[0] , "–>", record[1]
    raw_input("")
