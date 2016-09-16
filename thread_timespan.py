from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
# here we assume that database.db only contains data from healingwell
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine
session = Session()

import numpy as np

# function to get time span in hours
from datetime import datetime
def get_time_span(thread):
    #post_timestamps = np.array([post.timestamp for post in thread.posts], dtype='datetime64')
    # assume the last post in thread.posts is the last reply
    thread_time = datetime.strptime(thread.timestamp, '%Y-%m-%d %H:%M:%S')
    if not thread.posts:
    	return 0
    last_reply_time = datetime.strptime(thread.posts[-1].timestamp, '%Y-%m-%d %H:%M:%S')
    time_delta = last_reply_time - thread_time
    #print(time_delta)
    #calculate the time span in hours
    time_span = 24*int(time_delta.days) + time_delta.seconds//3600
    if time_span < 0:
    	print('Found unusual thread, ID is %d' % thread.id)
    return time_span

num_thread = session.query(Thread).count()
thread_timespan = np.empty([1, num_thread],dtype="int32")
#thread_posts = np.array([len(thread.posts) for thread in threads])
for i in range(1, num_thread+1):
    thread = session.query(Thread).get(i)
    thread_timespan[0,i-1] = get_time_span(thread)
    if i%30==0:
        print("Processing %d/%d time span" % (i, num_thread))
print("Saving to file..")
np.save("outputs/thread_timespan_krebs", thread_timespan)
session.close()
