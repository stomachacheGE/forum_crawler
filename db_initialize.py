# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 21:47:38 2016

@author: Johnson
"""
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///database_krebs.db')
Base = declarative_base()

class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile_url = Column(String)
    posts = relationship('Post', backref='author')
    threads = relationship('Thread',backref='author')
    forum = Column(String)
    date_joined = Column(String)
    total_posts = Column(String)

    def __repr__(self):
        number_of_posts = len(self.posts)
        number_of_threads = len(self.threads)
        return 'User <%s> is from forum <%s>, has %d threads, %d posts.' \
                % (self.name, self.forum, number_of_threads, number_of_posts)
    
class Thread(Base):
    __tablename__ = 'threads'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    body = Column(String)
    timestamp = Column(String)
    title = Column(String)
    posts = relationship('Post', backref='thread')
    subforum = Column(String)
    subforum_url = Column(String)
    
    def __repr__(self):
        return '\nTitle: %s \nUser: %s \nTime: %s \nPosts: %d\nURL: %s \n%s \n' \
            % (str(self.title), self.author.name, self.timestamp, len(self.posts), self.url, self.body)

    
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    body = Column(String)
    timestamp = Column(String)
    thread_id = Column(Integer, ForeignKey('threads.id'))
    order_of_reply = Column(Integer)
    subforum = Column(String)
    subforum_url = Column(String)
    
    def __repr__(self):
        return '\nUser: %s \nTime: %s \nThread: %s \nOrder: %s \nURL: %s \n%s \n' \
                % (self.author.name, self.timestamp, str(self.thread.title), str(self.order_of_reply), self.url, self.body)
    
Base.metadata.create_all(engine)