from app.models import Prices
from app import create_app,db
import unittest


class TestUser(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()
		self.client = self.app.test_client()
		p = Prices(phone="Samsung",price="1200-1200")
		db.session.add(p)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.ctx.pop()

	def test_user(self):
		response = self.client.get("/")
		self.assertIsNotNone(response)
		self.assertTrue("Samsung" in response.get_data(as_text=True))

	def test_404(self):
		response = self.client.get("/root")
		self.assertTrue("Error" in response.get_data(as_text=True))

