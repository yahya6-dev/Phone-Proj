#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import os
from MySQLdb import connect
import re
from datetime import datetime
from scrapy.selector import Selector


def process_item(item,conn,cursor):
	TIME_STAMP = datetime.utcnow()
	for phone_detail in item["output"]:
			if phone_detail["price"]:
				price,detail = phone_detail["price"],phone_detail["name"]
				cursor.execute("insert into prices(phone,price,time_stamp) values(%s,%s,%s)",[re.sub("==","",detail),price,TIME_STAMP])
	conn.commit()

def connect_to_db(user,passwd,db,host,delete=False):
	try:
		conn = connect(os.getenv("DATABASE_URL"))	
	except Exception as e:
		print(e)
		raise SystemExit("cant connect")
	cursor = conn.cursor()
	if delete:
		cursor.execute("delete from prices")
		conn.commit()
	return cursor,conn

def main():
	url = "https://nigerianprice.com/slot-nigeria-price-list/"
	response = requests.get(url)
	selector = Selector(text=response.text,type="html")
	delete_db = False
	if response.status_code == 200:
		delete_db = True
	def parse_item(item):
		text = re.sub("(N[,0-9]+.*N[,0-9]+)","",item)
		price = re.search("(N[,0-9]+.*[,0-9]+)",item) 
		if text and price:
			return text,price.group(0)

	def parse(response):
		output = {"output":[]} 
		for item in response.xpath("//ul/li/text()"):
			text,price = parse_item(item.get())
			my_item = {}
			my_item['price'] = price
			my_item['name'] = text
			output["output"].append(my_item)
			print(my_item["price"])
		return output

	output = parse(selector)
	cursor,conn= connect_to_db(delete_db)
	process_item(output,conn,cursor)
	os._exit(0)
if __name__=="__main__":
	main()
