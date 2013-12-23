AwfulPy
=======

with great power comes great responsibility.

Usage
=======

from AwfulPy import AwfulPy

username, password = 'your_username', 'your_passwd'
ap = AwfulPy(username, passwd)

print(ap.index.listings)

the_pos = ap.index.forums['219']
the_pos.read()

print(the_pos.listings)

bad_thread = the_pos.threads['3596817']
bad_thread.read()

for post in bad_thread.posts:
  print(post.poster.name + " is a shitty poster. Don't post")
  print(post.body)

shitty_poster_profile = post.poster.url




Browsing threads
License
========

Modified GPLv3 w/ no commercial use w/o my consent + this clause must be applied to all derivatives, motherfuckers.
