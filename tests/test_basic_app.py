import unittest
from app import create_app,db
from flask import current_app

class test_basic_app(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")     #setup the app for a proper testing
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.ctx.pop()

	def test_app_exists(self):
		self.assertIsNotNone(current_app)

	def test_is_testing(self):
		self.assertTrue(current_app.config.get("TESTING"))
