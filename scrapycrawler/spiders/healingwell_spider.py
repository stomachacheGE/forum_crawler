import scrapy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
from bs4 import BeautifulSoup
#import html2text as ht
from datetime import datetime, date, timedelta
#log.start(loglevel='DEBUG', logstdout=False)
from scrapycrawler.items import UserItem, PostItem, ThreadItem

class HealingWellSpider(scrapy.Spider):
    name = "healingwell"
    forum_name = "healing well"
    allowed_domains = ["www.healingwell.com"]
    start_urls = ["http://www.healingwell.com/community/?f=35&p=%d" % n for n in range(740,1158)]

    HEALINGWELL = "http://www.healingwell.com"

    def parse(self, response):

        tablerows = response.css('tr')
        for row in tablerows:
            #print('The row')
            #print(row.css('td').extract())
            if (row.css('.msgTopicAnnounce.TopicTitle') and row.css('.msgTopic.TopicTitle')):
                continue

            if row.css('.msgTopicAnnounce.TopicTitle'):
                #print('GOT U')
                thread_page_url = self.HEALINGWELL + row.css('.msgTopicAnnounce.TopicTitle a::attr(href)').extract_first()
                yield scrapy.Request(thread_page_url, callback=self.parse_thread_page)
            elif row.css('.msgTopic.TopicTitle'):
                #print('GOT U')
                thread_page_url = self.HEALINGWELL + row.css('.msgTopic.TopicTitle a::attr(href)').extract_first()
                yield scrapy.Request(thread_page_url, callback=self.parse_thread_page)
            else:
                pass

    def parse_thread_page(self, response):
        posts = response.css('.PostBox')
        number_of_posts = len(posts)

        thread_author = UserItem()
        thread_author['profile_url'] = self.HEALINGWELL + posts[0].css('.msgUser a[href]::attr(href)').extract_first()
        thread_author['name'] = posts[0].css('.msgUser a[href]::text').extract_first()
        thread_author['date_joined'] = posts[0].css('.msgUserInfo::text').extract()[0]
        thread_author['total_posts'] = posts[0].css('.msgUserInfo::text').extract()[1]
        thread_author['forum'] = self.forum_name
        yield thread_author

        thread = ThreadItem()
        thread['url'] = response.url
        thread['title'] = response.css('#PageTitle h1::text').extract_first()
        thread['author'] = thread_author
        thread['body'] = self.body_parser(posts[0].css('.PostMessageBody').extract_first())
        thread['timestamp'] = self.time_parser(posts[0].css('.PostThreadInfo ::text').extract_first())
        yield thread

        for i in range(number_of_posts):
            if i >= 1:
                post_author = UserItem()
                post_author['profile_url'] = self.HEALINGWELL + posts[i].css('.msgUser a[href]::attr(href)').extract_first()
                post_author['name'] = posts[i].css('.msgUser a[href]::text').extract_first()
                post_author['date_joined'] = posts[i].css('.msgUserInfo::text').extract()[0]
                post_author['total_posts'] = posts[i].css('.msgUserInfo::text').extract()[1]
                post_author['forum'] = self.forum_name
                yield post_author

                post = PostItem()
                post['url'] = response.url
                post['body'] = self.body_parser(posts[i].css('.PostMessageBody').extract_first())
                post['timestamp'] = self.time_parser(posts[i].css('.PostThreadInfo ::text').extract_first())
                post['thread_url'] = response.url
                post['author'] = post_author
                yield post

        pages_url = set(response.css('b a[href]::attr(href)').extract())

        for page in pages_url:
            page_url = self.HEALINGWELL + page
            yield scrapy.Request(page_url, callback=self.parse_post_page)


    def parse_post_page(self, response):
        posts = response.css('.PostBox')
        number_of_posts = len(posts)

        for i in range(number_of_posts):
                post_author = UserItem()
                post_author['profile_url'] = self.HEALINGWELL + posts[i].css('.msgUser a[href]::attr(href)').extract_first()
                post_author['name'] = posts[i].css('.msgUser a[href]::text').extract_first()
                post_author['date_joined'] = self.date_joined_parser(posts[i].css('.msgUserInfo::text').extract()[0])
                post_author['total_posts'] = self.total_posts_parser(posts[i].css('.msgUserInfo::text').extract()[1])
                post_author['forum'] = self.forum_name
                yield post_author

                post = PostItem()
                post['url'] = response.url
                post['body'] = self.body_parser(posts[i].css('.PostMessageBody').extract_first())
                post['timestamp'] = self.time_parser(posts[i].css('.PostThreadInfo ::text').extract_first())
                parts = response.url.split('&')
                post['thread_url'] = parts[0] + '&' + parts[1] 
                post['author'] = post_author
                yield post

    def body_parser(self, body):
        if body.find('<hr class="PostHR">') != -1:
            body = body[:body.find('<hr class="PostHR">')]
        body = body.replace("<br>","NEWLINE")
        soup = BeautifulSoup(body, 'html.parser')
        text = soup.get_text()
        return text.replace("NEWLINE", "\n")    
        #for br in soup.find_all("br"):
        #    br.replace_with("\n")
        #return soup.get_text()

    def date_joined_parser(self, body):
        body = body.replace('\xa0',' ')
        parts = body.split(' ')
        return parts[-1] + ' ' + parts[-2]

    def total_posts_parser(self, body):
        parts = body.split(':')
        return parts[-1][1:]

    def time_parser(self, body):
        parts = body.split()
        if parts[1] == 'Today':
            today = datetime.today()
            date = [today.month, today.day, today.year]
        elif parts[1] == 'Yesterday':
            today = datetime.today() - timedelta(1)
            date = [today.month, today.day, today.year]
        else:
            date = parts[1].split('/')
            date = [int(x) for x in date]
        time = parts[2].split(':')
        time = [int(x) for x in time]
        if parts[3] == 'PM':
            time[0] += 12
            if time[0] ==24:
                time[0] = 0
        dtime = datetime(date[2], date[0], date[1], time[0], time[1])
        return dtime.isoformat(sep=' ')
            #yield item

        #next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        #if next_page:
         #   url = response.urljoin(next_page[0].extract())
          #  yield scrapy.Request(url, self.parse_articles_follow_next_page)