# Author: Clinton Daniel, University of South Florida
# Narrator: Andrew Donnelly, University of South Florida
# Date: 11/26/2023
# Description: This is a Flask App that uses SQLite3 to
# execute (C)reate, (R)ead, (U)pdate, (D)elete operations

#Flask uses this app.py as the python file that will receive all the Http requests.
from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
#The code below is creating a function called "home". This will return the home.html page as found in the "templates" folder
def home():
    return render_template("home.html")


# Route to the form that's used to add a new student to the database
@app.route("/enternew")
#the code below defines a new function called "enterNew" that renders the "student.html" page as found in the templates folder
def enternew():
    return render_template("student.html")

# Route to insert a new student record into the students table in database.db
@app.route("/addrec", methods = ['POST', 'GET'])
    # Data will be available from POST submitted by the form on the student.html page.
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            # Once the data is collected from the form, it should connect to the database.db file and insert as a new record.
            # Connect to SQLite3 database and execute the INSERT. SQLite is used to create sql queries in the database.db
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (name, addr, city, zip) VALUES (?,?,?,?)",(nm, addr, city, zip))

                con.commit()
                msg = "Record successfully added to database"
        # 
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            # Whether successful or not, the page will display a message that should state the content in result.html
            return render_template('result.html',msg=msg)

#Route to SELECT all data from the database and display in a table      
#The route below is referencing the "Review and Edit students" button in the navigation bar
#this can be found if you go back to the layout.html page
@app.route('/list')

# the below code will create a function that creates a list details of all the records found in 
# the students table in database.db
def list():
    # SELECT rowid and all Rows from the students table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM students")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the list.html page
    return render_template("list.html",rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
# the below code will create a function that will overwrite a record with new details found in 
# a specific row in the students table in database.db
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM students WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html which is were the data is sent, overwriting the previous record.
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE students SET name='"+nm+"', addr='"+addr+"', city='"+city+"', zip='"+zip+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE students SET name="+nm+", addr="+addr+", city="+city+", zip="+zip+" WHERE rowid="+rowid

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # grab the id from the hidden variable in the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM students WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)