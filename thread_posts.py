from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_initialize import *
# here we assume that database.db only contains data from healingwell
engine = create_engine('sqlite://///Users/Johnson/Documents/nit/thesis/forum_crawler/database.db')
Session = sessionmaker(bind=engine)
Base.metadata.bind = engine
session = Session()

from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib2tikz import save as tikz_save
import numpy as np

threads = session.query(Thread).all()
thread_posts = np.array([len(thread.posts) for thread in threads])

post_bitcount = np.bitcount(thread_posts)
post_prob = post_bitcount / len(threads)
style.use('ggplot')
plt.yscale('log')
plt.xscale('log')
plt.title('Distribution of the number of replies to threads in the forum.')
plt.xlabel(r'Number of replies $N$')
plt.ylabel(r'Prob. that a thread has $N$ replies')
#plt.plot(np.arange(len(post_prob)), post_prob, 'ro', label='Inital Posts')
plt.legend()
plt.grid(True)

tikz_save('test.tex')