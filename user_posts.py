from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
# here we assume that database.db only contains data from healingwell
engine = create_engine('sqlite://///Users/Johnson/Documents/nit/thesis/forum_crawler/database.db')
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine
session = Session()

import numpy as np

users = session.query(User).all()


num_user = session.query(User).count()
user_posts = np.empty([1, num_user],dtype="int32")
#post_posts = np.array([len(post.posts) for post in posts])
for i in range(1, num_user+1):
    user = session.query(User).get(i)
    user_posts[0,i-1] = len(user.threads) + len(user.posts)
    if i%30==0:
        print("Processing %d/%d" % (i, num_user))
print("Saving to file..")
np.save("user_posts", user_posts)
session.close()

