# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class UserItem(scrapy.Item):
	name = scrapy.Field()
	profile_url = scrapy.Field()
	date_joined = scrapy.Field()
	total_posts = scrapy.Field()

class ThreadItem(scrapy.Item):
	url = scrapy.Field()
	body = scrapy.Field()
	timestamp = scrapy.Field()
	title = scrapy.Field()
	author = scrapy.Field()

class PostItem(scrapy.Item):
	url = scrapy.Field()
	body = scrapy.Field()
	timestamp = scrapy.Field()
	thread_url = scrapy.Field()
	author = scrapy.Field()
	order_of_reply = scrapy.Field()