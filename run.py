# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 23:49:07 2016

@author: Johnson
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *

engine = create_engine('sqlite://///Users/Johnson/Documents/nit/thesis/forum_crawler/database.db')
Session = sessionmaker(bind=engine)
session = Session()

#user = User(name='fu')
#user1 = User(name='andi')
#thread = Thread(body='This is a thread', author=user1)
#post = Post(body='This is a response', author=user, thread=thread)
users = session.query(User).order_by(User.name).all()

print('Found %d users \n' % len(users))
for user in users:
    print(user)

posts = session.query(Post).all()
print('Found %d posts \n' % len(posts))
#for post in posts:
#    print(post)  

threads = session.query(Thread).all()
print('Found %d threads \n' % len(threads))
#for thread in threads:
#    print(thread)  

session.close()