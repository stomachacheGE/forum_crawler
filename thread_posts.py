from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
# here we assume that database.db only contains data from healingwell
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine
session = Session()

import numpy as np

threads = session.query(Thread).all()
num_thread = session.query(Thread).count()
thread_posts = np.empty([1, num_thread],dtype="int32")
print(thread_posts)
#thread_posts = np.array([len(thread.posts) for thread in threads])
for i in range(1, num_thread+1):
    thread = session.query(Thread).get(i)
    thread_posts[0,i-1] = len(thread.posts)
    if i%2==0:
        print("%d/%d thread posts" % (i,num_thread))
print("Saving to file..")
np.save("outputs/thread_posts_krebs", thread_posts)
session.close()

