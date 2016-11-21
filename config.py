import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

class Auth:
	CLIENT_ID = ('27255012554-s0r870i3qr7d64s7bffm44stjml0b27b.apps.googleusercontent.com')
	CLIENT_SECRET = 'uK940ssVv6DJOmS51nm5OW5R'
	REDIRECT_URI = 'https://localhost:5000/gCallback'
	AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
	TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
	USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
	SCOPE = ['profile', 'email']

class Config:
	APP_NAME = "Python Project SZ CB"
	SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
	
