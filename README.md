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
  print(post.poster.name + " is a shitty poster. Don't post")
  print(post.body)

shitty_poster_profile = post.poster.url

my_bad_post = "Dear Richard,"
threadid = bad_thread.id

ap.session.reply(threadid, my_bad_post)


```

Try out AwfulGUI

```python
from AwfulPy import AwfulPy

username, passwd = 'your_username', 'your_passwd'
ap = AwfulPy(username, passwd)

from PyQt5 import QtWidgets
from sys import argv

app = QtWidgets.QApplication(argv)

from AwfulGUI.AwfulIndex import AwfulIndex

awfully_gui = AwfulIndex(ap)
awfully_gui.show()

#start crying
```

TODO
====

+ metatodo: name features to be fleshed out. add method signatures. raise NotImplmentedError.
+ compile list of methods raising the exception and add it here.



License
========

Modified GPLv3 w/ no commercial use w/o my consent + this clause must be applied to all derivatives, motherfuckers.
