from config import Auth
from app import app
import json
import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

def get_google_auth(state=None, token=None):
	if token:
		return OAuth2Session(Auth.CLIENT_ID, token=token)
	if state:
		return OAuth2Session(Auth.CLIENT_ID, state=state, redirect_uri = Auth.REDIRECT_URI)
	oauth = OAuth2Session(Auth.CLIENT_ID, redirect_uri = Auth.REDIRECT_URI, scope=Auth.SCOPE)
	return oauth

@app.route('/')
def landing():
	return render_template('landing.html')

@app.route('/home/')
@login_required
def home():
	return render_template('home.html') 

@app.route('/about/')
def about():
	return render_template('about.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	google = get_google_auth()
	auth_url, state = google.authorization_url(Auth.AUTH_URI, access_type='offline')
	session['oauth_state'] = state
	return render_template('login.html', auth_url=auth_url)

@app.route('/gCallback')
def callback():
	#redirects user to home page if already logged in
	if current_user is not None and current_user.is_authenticated:
		return redirect(url_for('home'))
	if 'error' in request.args:
		if request.args.get('error') == 'access_denied':
			return 'You are denied access.'
		return 'Error encountered.'
	if 'code' not in request.args and 'state' not in request.args:
		return redirect(url_for('login'))
	else:
		#exxecution reaches here when user has successfully authenticated our app
		google = get_google_auth(state=session['oauth_state'])
		try:
			token = google.fetch_token(Auth.TOKEN_URI, client_secret=Auth.CLIENT_SECRET, authorization_response=request.url)
		except HTTPError:
			return 'HTTPError occured.'
		google = get_google_auth(token = token)
		resp = google.get(Auth.USER_INFO)
		if resp.status_code == 200:
			user_data = resp.json()
			email = user_data['email']
			user = User.query.filter_by(email=email).first()
			if user is None:
				user = User()
				user.email = email
			user.name = user_data['name']
			print(token)
			user.tokens = json.dumps(token)
			user.avatar = user_data['picture']
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('home'))
		return 'Could not fetch your information.'

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('landing'))

	

