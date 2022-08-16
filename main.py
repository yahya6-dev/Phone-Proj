from app import create_app,db
from flask_migrate import Migrate,upgrade
import os
import click
import coverage
import sys
from app.models import Prices


COV = None
if os.getenv("COVERAGE"):					#checking for COVERAGE setting and configures it properly 
	COV = coverage.coverage(branch=True,include="app/*")

app = create_app( os.getenv("APP_CONFIG") or "development" )
migrate = Migrate(app,db)

@app.cli.command()
@click.option("--coverage/--no-coverage",default=False,help="run test under test coverage")     #run test configure test coverage
def test(coverage):										 #command line COVERAGE
	import unittest
	tests = unittest.TestLoader().discover("tests")
	unittest.TextTestRunner(verbosity=6).run(tests)

	if coverage  and not os.getenv("COVERAGE"):
		os.environ["COVERAGE"] = '1'
		os.execv(sys.executable,[sys.executable]+sys.argv)
	if COV:
		COV.stop()
		COV.save()
		COV.report()
		COV.erase()

@app.shell_context_processor
def make_context():
	return {"Price":Prices,"db":db}
