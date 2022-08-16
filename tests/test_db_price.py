from app import create_app,db
from app.models import Prices
import unittest

class TestAppDB(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()


	def tearDown(self):
		db.drop_all()
		db.session.remove()
		self.ctx.pop()

	def test_adding(self):
		u = Prices(phone="NOkia",price="1000")
		db.session.add(u)
		db.session.commit()
		self.assertTrue(Prices.query.first() !=None)
