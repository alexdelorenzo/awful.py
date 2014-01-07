AwfulPy
=======

works with python 2.7 and 3.3, probably everything in between as well. 

SATools -> forums session, methods, and scraper. 

AwfulGUI -> PyQt5 front-end to SATools. work in progress. py3k only.

don't get this banned. thanks.

Usage
=======


SATools

```python
from AwfulPy import AwfulPy

username, passwd = 'your_username', 'your_passwd'
ap = AwfulPy(username, passwd) # pass 'save_session=False' if you're paranoid

print(ap.index.listings)

the_pos = ap.index.forums['219']
the_pos.read()

print(the_pos.listings)

bad_thread = the_pos.threads['3596817']
bad_thread.read()

for post in bad_thread.posts.values():
  print(post.poster.name + "'s post:")
  print(post.body)

poster_profile = post.poster.url

my_bad_post = "Dear Richard,"
threadid = bad_thread.id

ap.session.reply(threadid, my_bad_post)


```

TODO
====



License
========

Modified GPLv3 w/ no commercial use w/o my consent + this clause must be applied to all derivatives.
