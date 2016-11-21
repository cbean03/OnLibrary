from app import db
from app import lm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import datetime

class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	name = db.Column(db.String(100), nullable=True)
	avatar = db.Column(db.String(200))
	active = db.Column(db.Boolean, default=False)
	tokens = db.Column(db.Text)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

@lm.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

