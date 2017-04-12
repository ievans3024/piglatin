import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from .piglatin import translatePhrase

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	pw_hash = db.Column(db.String(255), nullable=False)
	confirmed = db.Column(db.Boolean, default=False)
	registered_on = db.Column(db.DateTime, nullable=False)
	confirmed_on = db.Column(db.DateTime)

	def __init__(self, email, password, confirmed=False):
		self.email = email
		self.set_password(password)
		self.registered_on = datetime.datetime.now()

		# Confirm the user account
		if confirmed:
			self.confirm()

	def set_password(self, password):
		'''Hash the password'''
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		'''Confirmed the password'''
		return check_password_hash(self.pw_hash, password)

	def confirm(self):
		'''Confirm the user'''
		self.confirmed = True
		self.confirmed_on = datetime.datetime.now()

	@property
	def serialize(self):
		return {
			'id': self.id,
			'email': self.email
		}

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	original = db.Column(db.Text)
	translation = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id') )
	user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, original, user_id):
		self.original = original
		self.set_translation(original)
		self.user_id = user_id

	def set_translation(self, text):
		self.translation = translatePhrase(text)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'original': self.original,
			'translation': self.translation,
			'user_id': self.user_id
		}
