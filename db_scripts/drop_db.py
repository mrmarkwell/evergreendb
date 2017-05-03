# Author: Matthew Markwell
# Date: 5/2/2017
# 
# This file drops the database.
# By default it drops the database testevergreendb.
# Optionally, it will drop a different database passed in on the command line.

import MySQLdb as db
import sys

db_name = "testevergreendb"
if (len(sys.argv) > 1):
    db_name = sys.argv[1]

# Create the database if it doesn't exist
con = db.connect(user='aaaa', passwd='aaaa', use_unicode=True)
cur = con.cursor()
drop_cmd = "DROP DATABASE %s" % db_name
cur.execute(drop_cmd)

