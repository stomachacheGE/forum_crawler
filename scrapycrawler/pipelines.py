# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *

class ScrapycrawlerPipeline(object):

    def __init__(self, db_path):
        self.db_path = db_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_path=crawler.settings.get('DB_PATH'),
        )

    def open_spider(self, spider):
        self.engine = create_engine('sqlite:////'+self.db_path)
        print('sqlite:////'+self.db_path)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def close_spider(self, spider):
        #self.session.commit()
        self.session.close()
        self.engine.dispose()

    def process_item(self, item, spider):
        #self.db[self.collection_name].insert(dict(item))
        if item.__class__.__name__ == 'UserItem':
            #print('Found user %s \n' % item['name'])
            if not self.user_duplicate(item):
                print('Found new user')
                if item['forum'] == 'healing well':
                    new_user = User(name=item['name'], profile_url=item['profile_url'], forum=item['forum'],
                                    date_joined=item['date_joined'], total_posts=item['total_posts'])
                elif item['forum'] == 'prostatakrebs':
                    new_user = User(name=item['name'], profile_url=item['profile_url'], forum=item['forum'])
                else:
                    pass
                self.session.add(new_user)
                self.session.commit()
        elif item.__class__.__name__ == 'ThreadItem':
            author = self.session.query(User).filter_by(name=item['author']['name'], forum=item['author']['forum']).first()
            if not self.thread_duplicate(item):
                if item['author']['forum']== 'healing well':
                    new_thread = Thread(user_id=author.id, title=item['title'], url=item['url'],
                                      body=item['body'], timestamp=item['timestamp'])
                elif item['author']['forum'] == 'prostatakrebs':
                    new_thread = Thread(user_id=author.id, title=item['title'], url=item['url'],
                                      body=item['body'], timestamp=item['timestamp'], 
                                      subforum=item['subforum'], subforum_url=item['subforum_url'])
                else:
                    pass

                self.session.add(new_thread)
                self.session.commit()
        elif item.__class__.__name__ == 'PostItem':
            author = self.session.query(User).filter_by(name=item['author']['name'], forum=item['author']['forum']).first()
            thread = self.session.query(Thread).filter_by(url=item['thread_url']).first()
            print(author.id)
            print(thread.id)
            if not self.post_duplicate(item, author):
                if item['author']['forum'] == 'healing well':
                    new_post = Post(user_id=author.id, thread_id=thread.id, url=item['url'],
                                    body=item['body'], timestamp=item['timestamp'])
                elif item['author']['forum'] == 'prostatakrebs':
                    new_post = Post(user_id=author.id, thread_id=thread.id, url=item['url'],
                                    body=item['body'], timestamp=item['timestamp'], order_of_reply=item['order_of_reply'],
                                    subforum=item['subforum'], subforum_url=item['subforum_url'])
                else:
                    pass

                self.session.add(new_post)
                self.session.commit()
        else:
            pass

        return item

    def user_duplicate(self, user):
        get_user = self.session.query(User).filter_by(name=user['name'], forum=user['forum']).first()
        return True if get_user else False

    def post_duplicate(self, post, author):
        get_post = self.session.query(Post).filter_by(user_id=author.id, timestamp=post['timestamp']).first()
        return True if get_post else False

    def thread_duplicate(self, thread):
        get_thread = self.session.query(Thread).filter_by(url=thread['url']).first()
        return True if get_thread else False
