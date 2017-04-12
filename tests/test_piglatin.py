import unittest, json, os
from flask import current_app
from app import create_app, db

class BasicTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client()

	def load_fixtures(self, path, model_cls):
		fh = open(path)
		fixture = json.load(fh)
		fh.close()

		for data in fixture:
			instance = model_cls(**data)
			db.session.add(instance)
			db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):
		'''App Exists'''
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		'''App is testing'''
		self.assertTrue(current_app.config['TESTING'])
