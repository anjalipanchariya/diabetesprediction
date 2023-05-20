# Store this code in 'app.py' file
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pickle
import PyPDF2
from werkzeug.utils import secure_filename
import hashlib
import os
from flask import Flask, render_template, send_from_directory
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import plotly.graph_objects as go
from flask import Flask, render_template, request
import smtplib
import pdfkit
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# from pdf2image import convert_from_path


app = Flask(__name__)


app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'loginreg'

mysql = MySQL(app)

sess = {'log':False}
@app.route('/')
def main():
	msg = ""
	return render_template("home.html", msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
	global sess
	# print("Anjali")
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		h = hashlib.md5(password.encode()).hexdigest()
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND passwrd = % s', (username, h, ))
		account = cursor.fetchone()
		print(username)
		print(password)
		print("Anjali")
		if account:
			session['loggedin'] = sess['log'] = True
			session['id'] = sess['id'] =  account['id']
			session['username'] = sess['username'] = account['username']
			return render_template('home.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login2.html')

@app.route('/logout')
def logout():
	sess['log'] = False
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		h = hashlib.md5(password.encode()).hexdigest()
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, h, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			
			return render_template('login2.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register2.html', msg = msg)

@app.route('/manual', methods =['GET', 'POST'])
def manual():
	uid = ""
	global sess
	if sess['log'] == True:

		uid = sess['id'] 
		msg = []
		if request.method == 'POST' and 'age' in request.form and 'weight' in request.form 	and 'value1' in request.form and 'value2' in request.form and 'gender' in request.	form and 'date' in request.form:
			age = int(request.form['age'])
			gender = int(request.form['gender'])
			value1 = int(request.form['value1'])
			value2 = int(request.form['value2'])
			weight = int(request.form['weight'])
			date = request.form['date']
			print(date)
			if value1<100:
				severity1 = "Normal"
			elif value1>=100 and value1<=125:
				severity1 = "Pre-Diabetic"
			elif value1>125:
				severity1="Diabetic"
			else:
				severity1=""

			if value2<140:
				severity2 = "Normal"
			elif value2>=140 and value2<=199:
				severity2 = "Pre-Diabetic"
			elif value2>200:
				severity2="Diabetic"
			else:
				severity2=""
			
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

			cursor.execute('INSERT INTO rd VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s)', (age, value1, value2, weight, gender, severity1, severity2, uid,  date))
			mysql.connection.commit()
			msg.append('You have successfully added!')

			fig1 = go.Figure(go.Indicator(
			mode = "gauge+number",
			value = value1,
			domain = {'x': [0, 1], 'y': [0, 1]},
			title = {'text': "Glucose Fasting mg/dL", 'font': {'size': 24}},
			# delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
			gauge = {
			'axis': {'range': [None, 200], 'tickwidth': 1, 'tickcolor': "black"},
			'bar': {'color': "black",'thickness':0.25},
			'bgcolor': "white",
			'borderwidth': 2,
			'bordercolor': "black",
			'steps': [
            {'range': [0, 100], 'color': 'green'},
            {'range': [100, 125], 'color': 'yellow'},
			{'range': [125, 200], 'color': 'red'}]
        }))
			msg.append(f'You are {severity1}')

			fig1.write_image("static/image/fig2.png")

			fig2 = go.Figure(go.Indicator(
			mode = "gauge+number",
			value = value2,
			domain = {'x': [0, 1], 'y': [0, 1]},
			title = {'text': "Glucose Postprandial mg/dL", 'font': {'size': 24}},
			# delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
			gauge = {
			'axis': {'range': [None, 300], 'tickwidth': 1, 'tickcolor': "black"},
			'bar': {'color': "black",'thickness':0.25},
			'bgcolor': "white",
			'borderwidth': 2,
			'bordercolor': "black",
			'steps': [
            {'range': [0, 140], 'color': 'green'},
            {'range': [140, 200], 'color': 'yellow'},
			{'range': [200, 300], 'color': 'red'}]
        }))
			
			msg.append(f'You are {severity2}')
			fig2.write_image("static/image/fig3.png")

			return render_template('manual.html', fig1 = fig1, fig2 = fig2, msg = msg)
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
	else:
		return render_template('login2.html')
	return render_template('manual.html', msg = msg)

@app.route('/predictive', methods =['GET', 'POST'])
def predictive():
	msg = ''
	msg2 = ''
	if request.method == 'POST' and 'age' in request.form and 'bmi' in request.form and 'pre' in request.form and 'post' in request.form and 'gender' in request.form and 'family' in request.form and 'preg' in request.form and 'bp' in request.form :
		age = int(request.form['age'])
		bmi = int(request.form['bmi'])
		pre = int(request.form['pre'])
		post = int(request.form['post'])
		gender = int(request.form['gender'])
		family = int(request.form['family'])
		preg = int(request.form['preg'])
		bp = int(request.form['bp'])
		print(pre, post, bmi, bp, age, gender, family, preg)
		
		def predicts(pre, post, age, gender, bp, family, bmi, preg):
			print(pre, post, age, gender, bp, family, bmi, preg)
			loaded_model = pickle.load(open('model.sav', 'rb'))
			y = loaded_model.predict([[pre, post, age, gender, bp, family, bmi, preg]])
			print(y)
			return y[0][0]
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO pred VALUES (% s, % s, % s, % s, % s, % s, % s, % s)', (age, gender, pre, post, bmi, family, preg, bp))
		mysql.connection.commit()
		prediction = predicts(pre, post, age, gender, bp, family, bmi, preg)
		prediction = round(prediction,2)
		msg = f'The chances that you have diabetes are {prediction}%'
		if age<=30:
			agestr="0-30"
		elif age>30 and age<=50:
			agestr="31-50"
		else:
			agestr="51-100"
		
		if bmi<=18:
			bmistr="underweight"
		elif bmi>18 and bmi<=24:
			bmistr="normal"
		else:
			bmistr = "overweight"

		if prediction<=40:
			predstr="0-40"
		elif prediction>40 and prediction<=75:
			predstr="40-75"
		else:
			predstr="75-100"

		cursor.execute('select medRec, lifeRec, dietRec from recc WHERE age = % s AND bmi = % s AND pred = % s', (agestr, bmistr, predstr, ))

		fig = go.Figure(go.Indicator(
		mode = "gauge+number",
		value = prediction,
		domain = {'x': [0, 1], 'y': [0, 1]},
		# title = {'text': "Prediction", 'font': {'size': 24}},
		# delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
		gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "black"},
        'bar': {'color': "black",'thickness':0.25},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "black",
        'steps': [
            {'range': [0, 40], 'color': 'green'},
            {'range': [40, 75], 'color': 'yellow'},
			{'range': [75, 100], 'color': 'red'}]
        }))

		fig.write_image("static/image/fig1.png")
		data = cursor.fetchone()
		if data:
			print(data)
			print(type(data))
		return render_template('predsuccess.html', data=data, msg = msg, fig = fig)
		print(prediction)
		
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('predictive.html', msg = msg)



@app.route('/upload', methods =['GET', 'POST'])
def upload():
	global sess
	uid = ""
	if sess['log'] == True:
		uid = sess['id'] 

		upload_folder = "uploads/"+str(session['id'])
		if not os.path.exists(upload_folder):
			os.mkdir(upload_folder)
		app.config['UPLOAD_FOLDER'] = upload_folder
		msg =[]
		if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
			name = f.filename
			print("file uploaded successfully")
			msg=[]
			pdf_file = open("uploads/"+str(session['id'])+'/'+name, 'rb')
			pdf_reader = PyPDF2.PdfReader(pdf_file)


			def getseverity(range, value):
				pattern = r"\w+[-]?\w+:?[><]?=?\d+[-]?\d+"
				matches = re.findall(pattern, range)
				d = {}
				for i in matches:
					v = i.split(":")
					if '-' in v[-1]:
						d[v[0]] = v[-1].split('-')
					else:
						d[v[0]] = v[-1]
				severity = ''

				for k, v in d.items():
					if type(v) == str:
						if eval(str(value)+v):
							severity = k
							break
					else:
						if int(value)-int(v[-1]) <= 0:
							severity = k
							break
				return severity



			range1 = ''
			range2 = ''
			for page in range(len(pdf_reader.pages)):
				pdf_page = pdf_reader.pages[page]
				page_text = pdf_page.extract_text()

				lines = page_text.split()
				for i in range(len(lines)):
					if lines[i] == "Age:":
						age = int(lines[i+1])
					if lines[i] == "Gender:":
						gender = lines[i+1]
					if lines[i] == "Received:":
						date = "-".join(lines[i+1].split("/")[::-1])
					if lines[i] == "Weight:":
						weight = lines[i+1]
					if lines[i] == "Glucose" and lines[i+1:i+3] == ['Fasting', '(FBS)']:
						value1 = int(lines[i+3])
						unit1 = lines[i+4]
						range1 = lines[i+5:i+14]
					if lines[i] == "Glucose" and lines[i+1:i+3] == ['Postprandial', '(PPBS)']:
						value2 = int(lines[i+3])
						unit2 = lines[i+4]
						range2 = lines[i+5:i+13]
			range1 = "".join(range1)
			range2 = "".join(range2)
			severity1 = getseverity(range1, value1)
			severity2 = getseverity(range2, value2)
			if gender=='F':
				sex = 0
			elif gender=="M":
				sex=1

			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO rd VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s)', (age, value1, value2, weight, sex, severity1, severity2, uid, date))
			print("Added successfully")
			mysql.connection.commit()

			if age<=18:
				agestr="<=18"
			elif age>18 and age<=40:
				agestr="18-40"
			else:
				agestr=">40"
			print("Ready to fetch")
			# cursor.execute('select medicinal, diet, lifestyle, links from predrecc WHERE age 	= % s AND gender = % s AND 	severity1 = % s AND severity2 = % s', (agestr, 	sex, severity1, severity2, ))
			msg.append("Report record added successfully")
			# data = cursor.fetchone()
			# print(data,"*************************************")
			# if data:
			# 	print(data)
			# 	print(type(data))
			fig1 = go.Figure(go.Indicator(
			mode = "gauge+number",
			value = value1,
			domain = {'x': [0, 1], 'y': [0, 1]},
			title = {'text': "Glucose Fasting mg/dL", 'font': {'size': 24}},
			# delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
			gauge = {
			'axis': {'range': [None, 600], 'tickwidth': 1, 'tickcolor': "black"},
			'bar': {'color': "black",'thickness':0.25},
			'bgcolor': "white",
			'borderwidth': 2,
			'bordercolor': "black",
			'steps': [
            {'range': [0, 100], 'color': 'green'},
            {'range': [100, 125], 'color': 'yellow'},
			{'range': [125, 600], 'color': 'red'}]
        }))
			msg.append(f'You are {severity1}')

			fig1.write_image("static/image/fig4.png")

			fig2 = go.Figure(go.Indicator(
			mode = "gauge+number",
			value = value2,
			domain = {'x': [0, 1], 'y': [0, 1]},
			title = {'text': "Glucose Postprandial mg/dL", 'font': {'size': 24}},
			# delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
			gauge = {
			'axis': {'range': [None, 600], 'tickwidth': 1, 'tickcolor': "black"},
			'bar': {'color': "black",'thickness':0.25},
			'bgcolor': "white",
			'borderwidth': 2,
			'bordercolor': "black",
			'steps': [
            {'range': [0, 140], 'color': 'green'},
            {'range': [140, 200], 'color': 'yellow'},
			{'range': [200, 600], 'color': 'red'}]
        }))
			
			msg.append(f'You are {severity2}')
			fig2.write_image("static/image/fig5.png")
			return render_template('home.html',msg=msg)

			print(f"Age: {age}, Gender: {gender},weight: {weight},\n Value1: {value1}, unit1: 	{unit1}, severity: {severity1},	\n 	Value2: {value2}, unit2: {unit2}, 	severity2: {severity2}")

		elif request.method == 'POST':
			msg = 'Nothing to retrieve'
			return render_template('predsuccess.html', msg = msg)
	else:
		return render_template('login2.html')
	return render_template('upload.html',msg=msg)

global dir_path
dp = 'uploads/'
@app.route('/viewfile', methods =['GET', 'POST'])
def viewfile():
	global sess
	# global dp
	global dir_path
	uid = ""
	if sess['log'] == True:
		uid = session['id'] 
		dir_path = dp + str(uid)
		file_list = os.listdir(dir_path)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('select value1, value2, weight, age, reportdate from rd WHERE userid = % s', ([session['id']]))
		data = cursor.fetchall()
		return render_template('file_list.html', files=file_list, data = data)
	else:
		return render_template('login2.html')

@app.route('/files/<path:file_path>')
def view_file(file_path):
	global dir_path
	return send_from_directory(dir_path, file_path)

@app.route('/visualization', methods =['GET', 'POST'])
def visualization():
	
	def plot(t):
		v1, v2, w, d = [], [], [], []
		for i in t:
			v1.append(i['value1'])
			v2.append(i['value2'])
			w.append(i['weight'])
			d.append(str(i['reportdate']))
		date_time = pd.to_datetime(d)
		dataframe = pd.DataFrame(
		{'date_of_week': d, 'value1': v1, "value2": v2, "weight": w})

		fig, ax1 = plt.subplots(figsize=(8, 8))
		ax2 = ax1.twinx()

		l1 = ax1.plot(dataframe.date_of_week, dataframe.value1,
				marker="x", label="Value1", lw=2)
		l2 = ax1.plot(dataframe.date_of_week, dataframe.value2,
				lw=2, marker="x", label="Value2")
		l3 = ax2.plot(dataframe.date_of_week, dataframe.weight,
				lw=1, linestyle="--", marker="o", label="weight", color="green")

		ax1.set_xlabel("Date")
		ax1.set_ylabel("mg/dl")
		ax1.tick_params(axis="y")

		ax2.set_ylabel("Kg")
		ax2.tick_params(axis="y")
		ax1.legend(['Glucose fasting', 'Glucose postprandial'], loc='upper left',)
		ax2.legend(['weight'], loc='upper right',)
		ax2.set_ylim(0, 100)
		fig.suptitle("visualization", fontsize=20)
		fig.autofmt_xdate()
		# plt.show()
		plt.savefig(os.path.join('static', 'image', 'plot.png'))
	
	global sess
	# uid = sess['id']
	# print(uid)
	if sess['log'] == True:
		userid = session['id']
		print('userid', userid)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('select value1, value2, weight, reportdate from rd WHERE userid = % s ', ([session['id']]))
		msg = "Successful"
		data = cursor.fetchall()
		if data:
			print(data)
			# print(type(data))
			plot(data)

		return render_template('visualization.html')
		
	else:
		return render_template('login2.html')
	

# @app.route('/visualization')
# def index():
#     return render_template('visualization.html')

@app.route('/snapshot', methods=['POST'])
def snapshot():
    email = request.form['email']
    
    path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("templates\visualization.html", "report.pdf", configuration=config,)
    pdf_path = 'pdf\report.pdf'
    
    body = '''Hello,
    Below is the attatchement of your Visualized Report
    '''
    sender = 'anjalipanchariya11@gmail.com'
    password = 'atrnrjvhluqzhijg'
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = email
    message['Subject'] = 'Dia Recommendation - Visualized Report'

    message.attach(MIMEText(body, 'plain'))

    pdfname = 'report.pdf'
    binary_pdf = open(pdfname, 'rb')
    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload((binary_pdf).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    text = message.as_string()
    session.sendmail(sender, email, text)
    session.quit()
    print('Mail Sent')
    return render_template('visualization.html')

if __name__ == '__main__':
	app.run(debug=True)