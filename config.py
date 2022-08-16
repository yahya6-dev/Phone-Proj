import os
import uuid
import logging

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SQLALCHEMY_TRACK_MODIFICATIONS = True   #base for all configurations
	SECRET_KEY = uuid.uuid4().hex

	@classmethod
	def init_app(cls,app):			#special need to initialize app
		pass

class Testing(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite:///" #configuration for testing
	TESTING = True

class Development(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite://"+os.path.join(base_dir, os.getenv("DEV_DATABASE") or "dev_database.sqlite" ) #configuration for development

class Production(Config):
	USER = os.getenv("DB_USER")    #database credentials
	PASS = os.getenv("DB_PASS")
	HOST = os.getenv("DB_HOST")
	DB   = os.getenv("DB_NAME")
	PRODUCTION = True
	SQLALCHEMY_DATABASE_URI =  f"mysql://{USER}:{PASS}@{HOST}/{DB}"

	@classmethod
	def init_app(cls,app):
		from logging import StreamHandler
		handler = StreamHandler()
		handler.setLevel(logging.ERROR)
		app.logger.addHandler(handler)

config = {
		"testing":Testing,
		"development":Development,
		"production":Production

	}
