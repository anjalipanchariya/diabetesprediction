# Store this code in 'app.py' file
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Anjali@11'
app.config['MYSQL_DB'] = 'loginreg'

mysql = MySQL(app)

@app.route('/manualentry', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'age' in request.form and 'weight' in request.form and 'value1' in request.form and 'value2' in request.form and 'gender' in request.form :
		age = request.form['age']
		weight = request.form['weight']
		value1 = request.form['value1']
		value2 = request.form['value2']
		gender = request.form['gender']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		
		cursor.execute('INSERT INTO rd VALUES (%d, % d, % d, % d, %s)', (age, weight, value1, value2, gender, ))
		mysql.connection.commit()
		msg = 'You have successfully added!'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('manual.html', msg = msg)