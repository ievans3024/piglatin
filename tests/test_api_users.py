import unittest
import json
from app import create_app, db, mail
from app.models import User, Post
from app.api.authorization import generate_confirmation_token, confirm_token, verify_pwd
from app.api.resources import send_mail_with_token
from .test_piglatin import BasicTestCase

class APIUserTestCase(BasicTestCase):
	def setUp(self):
		super(APIUserTestCase, self).setUp()
		self.load_fixtures('tests/fixtures/users.json', User)

	def test_verify_password(self):
		'''Password verification'''

		# Correct Password
		self.assertTrue( verify_pwd('example@example.com', 'password') )

		# Wronge Password
		self.assertFalse( verify_pwd('example@example.com', 'sjadhfjskdhfak') )

		# Non Existing User
		self.assertFalse( verify_pwd('asda@example.com', 'klasdfalsdf') )

	def test_confirmation_token(self):
		'''Account confirmation token'''
		token = generate_confirmation_token('example@example.com')
		email = confirm_token(token)
		self.assertEqual( email, 'example@example.com' )

	def test_confirmation_token_email(self):
		''' Send Email with confirmation token'''
		token = generate_confirmation_token('example@example.com')

		with mail.record_messages() as outbox:
			send_mail_with_token('example@example.com', token)

			self.assertEqual( len(outbox), 1 )
			self.assertEqual( outbox[0].subject, "Account Verification")

	def test_create_user(self):
		'''User registration'''
		response = self.client.post('/api/v1/users',
			content_type='application/json',
			data=json.dumps({'email': 'new@example.com', 'password': 'password'}))

		self.assertEqual(response.status_code, 200)
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['email'], 'new@example.com')

		# User duplication
		response = self.client.post('/api/v1/users',
			content_type='application/json',
			data=json.dumps({'email': 'new@example.com', 'password': 'password'}))

	def test_user_confirmation(self):
		'''Account Activation'''
		email = 'example@example.com'

		# Email exists in the database
		user = User.query.filter_by(email=email).first()
		self.assertTrue(user)

		token = generate_confirmation_token(email)

		response = self.client.get('/api/v1/confirm/' + token,
					content_type='application/json',
					headers = {'Authorization': 'Basic ZXhhbXBsZUBleGFtcGxlLmNvbTpwYXNzd29yZA=='})

		self.assertEqual(response.status_code, 200)

		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['email'], email)

		user = User.query.filter_by(email=email).first()
		self.assertTrue(user.confirmed == True)
