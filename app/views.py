from app import app
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

@app.route('/')
def landing():
	return render_template('index.html')

@app.route('/home/')
def home():
	return render_template('home.html') 

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['password'] != 'password' or request.form['username'] != 'username':
			error = 'Invalid credentials, please try again'
		else:
			return redirect(url_for('home'))
	return render_template('login.html', error=error)	

