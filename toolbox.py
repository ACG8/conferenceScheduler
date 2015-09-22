#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
import MySQLdb
import getpass
import datetime

def connect():
    "Connect to the database of user's choice"
    usr = raw_input("User: ")
    passd = getpass.getpass()
    database = raw_input("Database: ")
    db = MySQLdb.connect(host="localhost", user=usr, passwd=passd, db=database)
    return db

def append(db, table):
    "Appends datum to table (string)"
    cursor  = db.cursor()
    cursor.execute("SHOW COLUMNS FROM {}".format(table))
    columns = cursor.fetchall()
    keyList = []
    valueList = []
    append0 = keyList.append
    append1 = valueList.append
    for column in columns:
        #print column
        if not ("auto_increment") in column:
            key = column[0]
            append0(column[0])
            if "datetime" in column: append1("'{}'".format(str(datetime.datetime.now())))
            else:
                value = raw_input('{}: '.format(key))
                if not value: value = "NULL"
                append1(value)
    keys = ",".join(keyList)
    values = ",".join(valueList)
    statement = "INSERT INTO {} ({}) VALUES ({});".format(table,keys,values)
    print statement
    cursor.execute(statement)

def commit(db):
    db.commit()
