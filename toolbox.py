0#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
import MySQLdb
import getpass
import datetime

class Connection:

    def __init__(self,user,password,database):
        self.user = user
        self.db = MySQLdb.connect(host="localhost", user=user, passwd=password, db=database)

    def getAttributes(self,table):
        "Returns the fields of the table and their associated datatypes"
        cursor = self.db.cursor()
        cursor.execute("SHOW COLUMNS FROM {}".format(table))
        columns = cursor.fetchall()
        columns = [c[:2] for c in columns]
        return columns

    def getTables(self):
        "Returns a list of tables in the database"
        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return tables

    def execute(self,statement):
        cursor = self.db.cursor()
        cursor.execute(statement)
        return cursor

    def update(self,table,CAs,CVs,FAs,FOs,FVs):
        "Changes each attribute in CAs to the value in CVs when filter FAs,FOs,FVs holds"
        
        whereStatement = getFilter(FAs,FOs,FVs)
        #you cannot update without a where statement or a matching set of change attributes and values
        if not (whereStatement): return "ERROR - FAILED TO PARSE FILTERS"
        if not (len(CAs)==len(CVs)): return "ERROR - ATTRIBUTE AND VALUE LIST LENGTHS DO NOT MATCH"
        for i,v in enumerate(CVs):
            try: CVs[i] = str(int(v))                        #Integers
            except ValueError: CVs[i] = "\"{}\"".format(v)   #Strings
        setStatement = ", ".join(["{} = {}".format(CAs[i],v) for i,v in enumerate(CVs)])
        query = "UPDATE {} SET {} WHERE {}".format(table,setStatement,whereStatement)
        cursor = self.db.cursor()
        cursor.execute(query)
        return "SUCCESS; {} UPDATED TO SET {} WHERE {}".format(table,setStatement,whereStatement)

    def select(self,table,SAs,FAs,FOs,FVs):
        "Returns the values of the requested SAs given filters FAs,FOs,FVs"
        whereStatement = getFilter(FAs,FOs,FVs)
        #you cannot update without a where statement or a matching set of change attributes and values
        if not (whereStatement): return "ERROR - FAILED TO PARSE FILTERS"
        selectStatement = ", ".join(SAs)
        if not selectStatement: selectStatement = "*"
        query = "SELECT {} FROM {} WHERE {}".format(selectStatement,table,whereStatement)
        cursor = self.db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def delete(self,table,FAs,FOs,FVs):
        "Deletes based on filters FAs,FOs,FVs"
        whereStatement = getFilter(FAs,FOs,FVs)
        #you cannot update without a where statement or a matching set of change attributes and values
        if not (whereStatement): return "ERROR - FAILED TO PARSE FILTERS"
        query = "DELETE FROM {} WHERE {}".format(table,whereStatement)
        cursor = self.db.cursor()
        cursor.execute(query)
        return "SUCCESSFUL DELETION"

    def selectAll(self,table,SAs):
        "Returns the entire table, with just attributes SAs"
        selectStatement = ", ".join(SAs)
        if not selectStatement: selectStatement = "*"
        cursor = self.db.cursor()
        cursor.execute("SELECT {} FROM {}".format(selectStatement,table))
        result = cursor.fetchall()
        return result

    def append(self,table,tuples,fields=None):
        "Appends given tuples to table"
        fieldStatement = ""
        if fields: fieldStatement = "({}) ".format(", ".join(fields))
        valuesStatement = ", ".join(tuples)
        statement = "INSERT INTO {} {}VALUES ({});".format(table,fieldStatement,valuesStatement)
        print(statement)
        cursor  = self.db.cursor()
        cursor.execute(statement)

    def commit(self):
        self.db.commit()


def sanitize(statement):
    "Sanitizes a statement by removing quotes and semicolns to prevent SQL injection attacks"
    return statement.replace(";","").replace("'","").replace("\"","")

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

#print "Connection automatically established with conferencescheduler connectionas 'db' for debugging purposes"
#db = Connection("ananda","password","scheduler")
