from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app,'mydb')
app.secret_key = '0118999881999119725'


@app.route('/')
def index():                         # run query with query_db()
    return render_template('index.html')

@app.route('/emailadd', methods=['POST'])
def create():
    email=request.form['email']
    if(len(email) < 1):
        flash("Email cannot be empty!")
        return redirect('/')
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!") 
        return redirect('/')
    query2 = "SELECT * FROM emails WHERE email_address=:email"
    query = "INSERT INTO emails (email_address, created_at, updated_at) VALUES (:email, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'email': email
           }
    # Run query, with dictionary values injected into the query.
    i = mysql.query_db(query2, data)

    if len(i)<1:
        mysql.query_db(query, data)
    else:
        flash("Email already exists")
    return redirect('/success')


@app.route('/emaildel', methods=['POST'])
def remove():
    email=request.form['email']
    if(len(email) < 1):
        flash("Email cannot be empty!")
        return redirect('/')
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!") 
        return redirect('/')

    query = "DELETE FROM emails WHERE email_address=:email"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'email': email
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_emails=emails)

app.run(debug=True)
