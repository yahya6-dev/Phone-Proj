from scrapy import Spider,Field,Item
import os
from MySQLdb import connect
from scrapy.exceptions import CloseSpider
import re
from scrapy.shell import inspect_response
from scrapy.settings import Settings
from datetime import datetime
class MyPipeline:
	def __init__(self,db,user,passwd,host):
		self.db = db
		self.user = user
		self.passwd = passwd
		self.host = host

	def process_item(self,item,crawler):
		TIME_STAMP = datetime.utcnow()
		for phone_detail in item["output"]:
			if phone_detail["price"]:
				price,detail = phone_detail["price"],phone_detail["name"]
				self.cursor.execute("insert into prices(phone,price,time_stamp) values(%s,%s,%s)",[re.sub("==","",detail),price,TIME_STAMP])
		self.conn.commit()

	def close_spider(self,crawler):
		self.cursor.close()
		self.conn.close()

	@classmethod
	def from_crawler(cls,crawler):
		return cls(os.getenv("DB"),
			os.getenv("USER"),
			os.getenv("PASSWD"),
			os.getenv("HOST"))

	def open_spider(self,crawler):
		try:
			self.conn =  connect(user=self.user,passwd=self.passwd,db=self.db,host=self.host)
		except:
			raise CloseSpider("Cant open the database")
		else:
			self.cursor = self.conn.cursor()

class MyItem(Item):
	name = Field()
	price = Field()

class PhonePrices(Spider):
	name = "price0"
	start_urls = ["https://nigerianprice.com/slot-nigeria-price-list/"]
	allowed_domains    = ["nigerianprice.com"]
	custom_settings = {
		"LOG_LEVEL":"ERROR",
		"ITEM_PIPELINES":{
			"phonePrice.MyPipeline":300
		}
	}



	def parse_item(self,item):
		text = re.sub("(N[,0-9]+.*N[,0-9]+)","",item)
		price = re.search("(N[,0-9]+.*[,0-9]+)",item) 
		if text and price:
			return text,price.group(0)

	def parse(self,response):
		output = {"output":[]} 
		for item in response.xpath("//ul/li/text()"):
			text,price = self.parse_item(item.get())
			my_item = MyItem()
			my_item['price'] = price
			my_item['name'] = text
			output["output"].append(my_item)
			print(my_item["price"])
		return output
