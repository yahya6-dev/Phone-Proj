from . import main
from flask import render_template
from ..models import Prices
from datetime import datetime
from flask import request

def is_mobile(user_agent):
	return "mobile" in user_agent.lower()

@main.route("/")
def index():
	items = Prices.query.order_by(Prices.phone).all()
	if is_mobile(request.headers.get("User-Agent")):
		return render_template("main1.html",last_update=items[0].time_stamp,phones=items)
	else:
		return render_template("main.html",last_update=items[0].time_stamp,phones=items)

@main.app_errorhandler(404)
def not_found(e):
	return render_template("404.html"),404

@main.app_errorhandler(500)
def internal_server(e):
	return render_template("500.html"),500
