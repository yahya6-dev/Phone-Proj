import os
import uuid
import logging

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SQLALCHEMY_TRACK_MODIFICATIONS = True   #base for all configurations
	SECRET_KEY = uuid.uuid4().hex
	SSL_REDIRECT = False
	@classmethod
	def init_app(cls,app):			#special need to initialize app
		pass

class Testing(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite:///" #configuration for testing
	TESTING = True

class Development(Config):
	SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE")  #configuration for development

class Production(Config):
	USER = os.getenv("DB_USER")    #database credentials
	PASS = os.getenv("DB_PASS")
	HOST = os.getenv("DB_HOST")
	DB   = os.getenv("DB_NAME")
	PRODUCTION = True
	SQLALCHEMY_DATABASE_URI =  os.getenv("DATABASE_URL").replace("postgres","postgresql")

	@classmethod
	def init_app(cls,app):
		from logging import StreamHandler
		from werkzeug.middleware.proxy_fix import ProxyFix
		handler = StreamHandler()
		handler.setLevel(logging.ERROR)
		app.logger.addHandler(handler)
		app.wsgi_app = ProxyFix(app.wsgi_app)

class Heroku(Production):
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace("postgres","postgresql")
	SSL_REDIRECT = True


config = {
		"heroku":Heroku,
		"testing":Testing,
		"development":Development,
		"production":Production

	}
