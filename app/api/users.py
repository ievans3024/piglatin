import datetime
from flask import jsonify, request, make_response
from . import api
from .. import db, mail
from ..models import User
from .authorization import auth, generate_confirmation_token, confirm_token

from flask_mail import Message

def send_mail_with_token(email, token):
	'''Send email with the confirmation token'''
	msg = Message()
	msg.add_recipient( email )
	msg.subject = 'Account Verification'
	msg.sender = "Pig Latin <admin@piglatin.com>"
	msg.body = 'Token Verification: ' + token
	mail.send( msg )

@api.route('/users', methods=['POST'])
def users_create():
	'''Create a new user'''
	request_data = request.get_json()

	user = User( request_data['email'], request_data['password'] )
	try:
		db.session.add(user)
		db.session.commit()
	except:
		abort(409)

	token = generate_confirmation_token(user.email)

	send_mail_with_token(user.email, token)

	return jsonify(user.serialize)

@api.route('/confirm/<token>', methods=['GET'])
@auth.login_required
def confirm_email(token):
	try:
		email = confirm_token(token)
	except:
		abort(401)

	user = User.query.filter_by(email=email).first()

	if user.confirmed:
		return jsonify({'status': 'already confirmed'})

	else:
		user.confirm()
		db.session.add(user)
		db.session.commit()

	return jsonify(user.serialize)
