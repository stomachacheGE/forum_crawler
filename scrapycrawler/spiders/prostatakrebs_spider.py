import scrapy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
#log.start(loglevel='DEBUG', logstdout=False)
from scrapycrawler.items import UserItem, PostItem, ThreadItem

class ProstatakrebsSpider(scrapy.Spider):
    name = "prostatakrebs"
    forum_name = "prostatakrebs"
    allowed_domains = ["forum.prostatakrebs-bps.de"]
    start_urls = ["http://forum.prostatakrebs-bps.de/forumdisplay.php?1-Prostatakrebs/"]

    PROSTATAKREBS = "http://forum.prostatakrebs-bps.de/"

    def parse(self, response):

        subforums = response.css('.forumbit_post.L1')
        for subforum in subforums:
            if subforum.css('.forumtitle a::attr(href)'):
                print('GOT U')
                forum_page_url = self.PROSTATAKREBS + self.url_check(subforum.css('.forumtitle a::attr(href)').extract_first())
                print(forum_page_url)
                yield scrapy.Request(forum_page_url, callback=self.parse_forum_page)

    def parse_forum_page(self, response):
        threads = response.css(".threadbit")

        for thread in threads:
            if thread.css("a.title::attr(href)"):
                thread_page_url = self.PROSTATAKREBS + self.url_check(thread.css("a.title::attr(href)").extract_first())
                yield scrapy.Request(thread_page_url, callback=self.parse_thread_page)

        next_page = response.css("a[rel=next]::attr(href)").extract_first()

        if next_page:
            next_page_url = self.PROSTATAKREBS + self.url_check(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_forum_page)


    def parse_thread_page(self, response):

        navs = response.css('li.navbit')
        subforum_url = self.PROSTATAKREBS + self.url_check(navs[2].css('a::attr(href)').extract_first())
        subforum = navs[2].css('a::text').extract_first()

        posttitle = response.css('h2.posttitle::text').extract_first()
        posts = response.css('.postbit')

        if posttitle:
            thread_author = UserItem()
            # if a user's profile_url is empty, this user is only a guest
            if self.url_check(posts[0].css('.username::attr(href)').extract_first()):
                thread_author['profile_url'] = self.PROSTATAKREBS + self.url_check(posts[0].css('.username::attr(href)').extract_first())
            else:
                thread_author['profile_url'] = ""
            # the username could be bold or not, depending on whether it is a registered user
            if posts[0].css('.username strong::text').extract_first():
                thread_author['name'] = posts[0].css('.username strong::text').extract_first()
            else:
                thread_author['name'] = posts[0].css('.username::text').extract_first()
            thread_author['forum'] = self.forum_name
            yield thread_author

            thread = ThreadItem()
            thread['url'] = response.url
            thread['title'] = response.css('.threadtitle a::text').extract_first()
            thread['author'] = thread_author
            thread['body'] = self.body_parser(posts[0].css('.postcontent').extract_first())
            thread['timestamp'] = self.datetime_parser(posts[0].css('.postdate').extract_first())
            thread['subforum_url'] = subforum_url
            thread['subforum'] = subforum
            yield thread

            del(posts[0]) # do not forget to delete the thread post

        for postitem in posts:

                post_author = UserItem()
                # if a user's profile_url is empty, this user is only a guest
                if self.url_check(postitem.css('.username::attr(href)').extract_first()):
                    post_author['profile_url'] = self.PROSTATAKREBS + self.url_check(postitem.css('.username::attr(href)').extract_first())
                else:
                    post_author['profile_url'] = ""
                if postitem.css('.username strong::text').extract_first():
                    post_author['name'] = postitem.css('.username strong::text').extract_first()
                else:
                    post_author['name'] = postitem.css('.username::text').extract_first()
                post_author['forum'] = self.forum_name
                yield post_author

                post = PostItem()
                post['url'] = response.url
                post['body'] = self.body_parser(postitem.css('.postcontent').extract_first())
                post['timestamp'] = self.datetime_parser(postitem.css('.postdate').extract_first())
                post['order_of_reply'] = postitem.css('.postcounter::text').extract_first()
                post['thread_url'] = self.thread_url_check(response.url.split('&')[0])
                post['author'] = post_author
                post['subforum_url'] = subforum_url
                post['subforum'] = subforum
                yield post


        next_page = response.css("a[rel=next]::attr(href)").extract_first()

        if next_page:
            next_page_url = self.PROSTATAKREBS + self.url_check(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_thread_page)


    def body_parser(self, body):
        if body.find('<hr class="PostHR">') != -1:
            body = body[:body.find('<hr class="PostHR">')]
        soup = BeautifulSoup(body, 'html.parser')
        return soup.get_text()


    def datetime_parser(self, date):
        soup = BeautifulSoup(date, 'html.parser')
        body = soup.get_text()
        body = body.replace('\xa0','')
        body = body.replace('\n','')
        parts = body.split(',')
        print(parts[0])
        if parts[0] == 'Heute':
            today = datetime.today()
            date_parts = [today.day, today.month, today.year]
        elif parts[0] == 'Gestern':
            day = datetime.today() - timedelta(1)
            date_parts = [day.day, day.month, day.year]
        else:
            date_parts = parts[0].split('.')
        time_parts = parts[1].split(':')
        dtime = datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]), int(time_parts[0]), int(time_parts[1]))
        return dtime.isoformat(sep=' ')

    def url_check(self, url):
        if url:
            return url.split('&')[0]
        else:
            return None

    def thread_url_check(self, url):
        parts = url.split('/')
        if parts[-1].find('page') != -1:
            del(parts[-1])
        return '/'.join(parts)
