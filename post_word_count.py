from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
# here we assume that database.db only contains data from healingwell
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine
session = Session()

import numpy as np

import re
def word_count(doc):
    count = len(re.findall(r'\w+', doc))
    return count

num_post = session.query(Post).count()
post_word_count = np.empty([1, num_post],dtype="int32")
#post_posts = np.array([len(post.posts) for post in posts])
for i in range(1, num_post+1):
    post = session.query(Post).get(i)
    post_word_count[0,i-1] = word_count(post.body)
    if i%30==0:
        print("Processing %d/%d post word count" % (i, num_post))
print("Saving to file..")
np.save("outputs/post_word_count_krebs", post_word_count)
session.close()
