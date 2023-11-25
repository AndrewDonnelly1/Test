# Author: Clinton Daniel, University of South Florida
# Narrator: Andrew Donnelly, University of South Florida
# Date: 4/4/2023
# Description: This python script assumes that you already have
# a database.db file at the root of your workspace.
# This python script will CREATE a table called students 
# in the database.db using SQLite3 which will be used
# to store the data collected by the forms in this app
# Execute this python script before testing or editing this app code. 
# Open a python terminal and execute this script:
# python create_table.py

import sqlite3

# We wil need to create the database.db before initiating the app.
#The below code is to connect the the database.db database which is where the table will be found.
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

#The below code will execute a command to create a table called, "students"
# that contains their name, address, city, and zip.
conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, zip TEXT)')
print("Created table successfully!")

conn.close()
#Once successfully executed, take a look at database.db so see the results.