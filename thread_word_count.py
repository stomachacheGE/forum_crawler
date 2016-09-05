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

num_thread = session.query(Thread).count()
thread_word_count = np.empty([1, num_thread],dtype="int32")
#thread_posts = np.array([len(thread.posts) for thread in threads])
for i in range(1, num_thread+1):
    thread = session.query(Thread).get(i)
    thread_word_count[0,i-1] = word_count(thread.body)
    if i%30==0:
        print("Processing %d/%d" % (i, num_thread))
print("Saving to file..")
np.save("thread_word_count", thread_word_count)
session.close()
