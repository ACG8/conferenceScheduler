0#!/usr/bin/python
# -*- coding: cp1252 -*-

# import MySQL module
import MySQLdb
import getpass
import datetime
from toolbox import *

def generateRooms(number)
    db = Connection("root","password","scheduler")

    #First, 
    buildings = ["AAA","BBB","CCC"]
    for b in buildings:
        i = 0
        for r in range(number):
            db.append("tbl_room_locations",()
