import unittest
import json
from app import create_app, db
from app.models import User, Post
from app.api.authorization import verify_pwd, generate_confirmation_token, confirm_token
from .test_piglatin import BasicTestCase

class APIPostTestCase(BasicTestCase):
	def setUp(self):
		super(APIPostTestCase, self).setUp()
		self.load_fixtures('tests/fixtures/users.json', User)
		self.load_fixtures('tests/fixtures/posts.json', Post)

		self.user = User('post@example.com', 'password')
		self.user.confirm()
		self.post = Post('my post test content', self.user.id)

		db.session.add(self.user)
		db.session.add(self.post)
		db.session.commit()

	def test_create_post_fail(self):
		'''Create post user not confirmed'''
		response = self.client.post('/api/v1/posts',
			content_type='application/json',
			headers = {'Authorization': 'Basic ZXhhbXBsZUBleGFtcGxlLmNvbTpwYXNzd29yZA=='},
			data=json.dumps({'original': 'my original test 2'}))

		self.assertEqual(response.status_code, 401)

	def test_create_post(self):
		'''Create a new post'''
		response = self.client.post('/api/v1/posts',
			content_type='application/json',
			headers = {'Authorization': 'Basic cG9zdEBleGFtcGxlLmNvbTpwYXNzd29yZA=='},
			data=json.dumps({'original': 'my original test'}))

		self.assertEqual(response.status_code, 200)

		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['original'], 'my original test')
		self.assertEqual(data['translation'], 'ymay originalway esttay')

	def test_get_post(self):
		'''Get post'''
		response = self.client.get('/api/v1/posts/' + str(self.post.id))

		self.assertEqual(response.status_code, 200)

		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['original'], 'my post test content')
		self.assertEqual(data['translation'], 'ymay ostpay esttay ontentcay')

	def test_update_post(self):
		'''Update a post'''
		post = Post('my post', self.user.id)
		db.session.add(post)
		db.session.commit()

		response = self.client.put('/api/v1/posts/' + str(post.id),
					content_type='application/json',
					headers = {'Authorization': 'Basic cG9zdEBleGFtcGxlLmNvbTpwYXNzd29yZA=='},
					data=json.dumps({'original': 'my original test'}))

		self.assertEqual(response.status_code, 200)

		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['original'], 'my original test')
		self.assertEqual(data['translation'], 'ymay originalway esttay')


	def test_delete_post(self):
		'''Delete a post'''

		post = Post('my post test content', self.user.id)
		db.session.add(post)
		db.session.commit()

		response = self.client.delete('/api/v1/posts/' + str(post.id),
					content_type='application/json',
					headers = {'Authorization': 'Basic cG9zdEBleGFtcGxlLmNvbTpwYXNzd29yZA=='})

		self.assertEqual(response.status_code, 200)

		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['result'], 1)

	def test_delete_invalide_post(self):
		'''Delete a invalide post'''
		response = self.client.delete('/api/v1/posts/' + str(500),
					content_type='application/json',
					headers = {'Authorization': 'Basic cG9zdEBleGFtcGxlLmNvbTpwYXNzd29yZA=='})
		self.assertEqual(response.status_code, 404)
