from flask import request, Response, make_response, jsonify
from functools import wraps
from flask_httpauth import HTTPBasicAuth
from ..models import User

from itsdangerous import URLSafeTimedSerializer

auth = HTTPBasicAuth()

def user_confirmed(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		user = User.query.filter_by(email=auth.username).first()
		if not user or not auth or not user.confirmed:
			return Response('Account is not confirmed', 401,{'WWW-Authenticate': 'Basic realm="Login Required"'})
		return f(*args, **kwargs)
	return decorated

@auth.verify_password
def verify_pwd(email, password):
	user = User.query.filter_by(email=email).first()
	if not user or not user.check_password(password):
		return False
	return True

@auth.error_handler
def unauthorized():
	return Response('Unauthorized access', 401,{'WWW-Authenticate': 'Basic realm="Login Required"'})

# Get the secret key here an the keep it a secre here from the app config

def generate_confirmation_token(email):
	serializer = URLSafeTimedSerializer('secret key here')
	return serializer.dumps(email, salt='keep it a secret')

def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer('secret key here')
	try:
		email = serializer.loads(
			token,
			salt='keep it a secret',
			max_age=expiration
		)
	except:
		return False
	return email
