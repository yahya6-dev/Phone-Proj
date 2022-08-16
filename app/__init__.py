from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config 
from threading import Timer
from flask_bootstrap import Bootstrap5
import os

db = SQLAlchemy() #set up db instance and
moment = Moment() #moment for proper time rendering
boostrap = Bootstrap5(None)

def run_schedule(s_time=60*60*2):
	def run():
		db.drop_all()
		db.create_all()
		os.system("scrapy runspider ../phonePrices.py")
		run_shedule()
	return Timer(s_time,run).start()

def create_app(config_name):
	app = Flask(__name__)               #create application factory
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	from .main import main
	app.register_blueprint(main)
	if not app.testing:
		run_schedule()

	boostrap.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	if not app.testing:
		run_schedule()
	return app




