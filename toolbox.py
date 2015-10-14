#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
import MySQLdb
import getpass
import datetime

def sanitize(statement):
    "Sanitizes a statement by removing quotes and semicolns to prevent SQL injection attacks"
    return statement.replace(";","").replace("'","").replace("\"","")
"""
def connect():
    "Connect to the database of user's choice"
    usr = raw_input("User: ")
    passd = getpass.getpass()
    database = raw_input("Database: ")
    db = MySQLdb.connect(host="localhost", user=usr, passwd=passd, db=database)
    return db
"""

def connect(usr,passd,database):
    "Connect to the given database"
    db = MySQLdb.connect(host="localhost", user=usr, passwd=passd, db=database)
    return db

def getAttributes(db,table):
    "Returns the fields of the table and their associated datatypes"
    cursor = db.cursor()
    cursor.execute("SHOW COLUMNS FROM {}".format(table))
    columns = cursor.fetchall()
    columns = [c[:2] for c in columns]
    return columns

def getTables(db):
    "Returns a list of tables in the database"
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return tables

def getFilter(attributes,operators,values):
    "Returns a properly formatted where clause"
    #Make sure all inputs have same length
    if not (len(attributes) == len(operators) == len(values)): return ""
    #Put quotations around strings and make sure strings operators are equals or not equals signs
    for i,v in enumerate(values):
        try: values[i] = str(int(v))        #Integers
        except ValueError:                  #Strings
            values[i] = "\"{}\"".format(v)
            if operators[i] not in ["=","!="]: return ""
    output = ", ".join(["{} {} {}".format(attributes[i],operators[i],v) for i,v in enumerate(values)])
    return output

def update(db,table,CAs,CVs,FAs,FOs,FVs):
    "Changes each attribute in CAs to the value in CVs when filter FAs,FOs,FVs holds"
    cursor = db.cursor()
    whereStatement = getFilter(FAs,FOs,FVs)
    #you cannot update without a where statement or a matching set of change attributes and values
    if not (whereStatement): return "ERROR - FAILED TO PARSE FILTERS"
    if not (len(CAs)==len(CVs)): return "ERROR - ATTRIBUTE AND VALUE LIST LENGTHS DO NOT MATCH"
    for i,v in enumerate(CVs):
        try: CVs[i] = str(int(v))                        #Integers
        except ValueError: CVs[i] = "\"{}\"".format(v)   #Strings
    setStatement = ", ".join(["{} = {}".format(CAs[i],v) for i,v in enumerate(CVs)])
    query = "UPDATE {} SET {} WHERE {}".format(table,setStatement,whereStatement)
    cursor.execute(query)
    return "SUCCESS; {} UPDATED TO SET {} WHERE {}".format(table,setStatement,whereStatement)

def select(db,table,SAs,FAs,FOs,FVs):
    "Returns the values of the requested SAs given filters FAs,FOs,FVs"
    whereStatement = getFilter(FAs,FOs,FVs)
    #you cannot update without a where statement or a matching set of change attributes and values
    if not (whereStatement): return "ERROR - FAILED TO PARSE FILTERS"
    selectStatement = ", ".join(SAs)
    if not selectStatement: selectStatement = "*"
    query = "SELECT {} FROM {} WHERE {}".format(selectStatement,table,whereStatement)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def selectAll(db,table,SAs):
    "Returns the entire table, with just attributes SAs"
    selectStatement = ", ".join(SAs)
    if not selectStatement: selectStatement = "*"
    cursor = db.cursor()
    cursor.execute("SELECT {} FROM {}".format(selectStatement,table))
    result = cursor.fetchall()
    return result

def append(db,table,tuples,fields=None):
    "Appends given tuples to table"
    fieldStatement = ""
    if fields: fieldStatement = "({}) ".format(", ".join(fields))
    valuesStatement = ", ".join(tuples)
    statement = "INSERT INTO {} {}VALUES {};".format(table,fieldStatement,valuesStatement)
    print statement
    cursor  = db.cursor()
    cursor.execute(statement)

#####To do: package everything into a class, db as property of class


def commit(db):
    db.commit()

def listCommands():
    "Lists all commands (and their arguments) in this module"
    print "sanitize(statement)"
    print "connect(usr,passd,database)"
    print "getAttributes(db,table)"
    print "getTables(db)"
    print "getFilter(attributes,operators,values)"
    print "update(db,table,CAs,CVs,FAs,FOs,FVs)"
    print "select(db,table,SAs,FAs,FOs,FVs)"
    print "selectAll(db,table)"
    print "append(db,table,tuples,fields=None)"
    print "commit(db)"
    print "listCommands()"
    

"""
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
"""

print "Connection automatically established with conferencescheduler as 'db' for debugging purposes"
db = connect("ananda","password","conferencescheduler")
