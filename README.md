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
In [1]: from AwfulPy import AwfulPy

In [2]: username = 'salisbury shake'

In [3]: ap = AwfulPy(username)
Loading from backup: .salisbury shake_sa.bak

In [4]: ap.
ap.index        ap.session      ap.session_bak  ap.username

In [4]: ap.index.
ap.index.base_url          ap.index.listings
ap.index.content           ap.index.section_listings
ap.index.forum_listings    ap.index.sections
ap.index.forums            ap.index.session

In [5]: pprint(ap.index.listings)
{'155': "SA's Front Page Discussion",
 '214': 'E/N Bullshit',
 '1': 'GBS 1.2',
 '154': "Synthy's Snack Shack",
 '26': 'FYAD: Cherry blossom petal landed in the lunch',
 '48': 'Main',

In [6]: the_pos = ap.index.forums['219']

In [7]: the_pos.read()

In [8]: the_pos.
the_pos.base_url   the_pos.listings   the_pos.pages      the_pos.session
the_pos.content    the_pos.name       the_pos.parent     the_pos.subforums
the_pos.id         the_pos.page       the_pos.read       the_pos.threads

In [9]: the_pos.listings
Out[13]: 
{'3136320': 'the yospos serious questions that arent serious enough for SHSC megathread',
 '3201527': 'Description: that darn feline.jpg',
 '3263403': 'Post the most worthless thing you can find on wikipedia',

In [10]: bad_thread = the_pos.threads['3136320']                                

In [11]: bad_thread.read()

In [11]: bad_thread.
bad_thread.          bad_thread.name      bad_thread.replies
bad_thread.author    bad_thread.page      bad_thread.session
bad_thread.base_url  bad_thread.pages     bad_thread.title
bad_thread.content   bad_thread.poster    bad_thread.url
bad_thread.icon      bad_thread.posts     bad_thread.views
bad_thread.id        bad_thread.rating    
bad_thread.lastpost  bad_thread.read      


In [12]: for post in bad_thread.posts.values():
   ....:       print(post.poster.name + "'s post:")
   ....:       print(post.body + '\n')
   ....:     
Jim Silly-Balls's post:
if youre like me and i know you are sometimes you have a computer related question but dont want to venture into SHSC to ask it because you would rather ask your friends in the pos.  this is the thread fo dat shit

CRIP EATIN BREAD's post:
it starts to shut down every two hours in march, and will expire in june 2010

In [13]: post.
post.body     post.id       post.poster   post.session  
post.content  post.parent   post.read     post.unread   

In [13]: post.poster.
post.poster.avatar_url  post.poster.name        post.poster.session
post.poster.content     post.poster.read        post.poster.title
post.poster.id          post.poster.reg_date    post.poster.url

In [13]: post.poster.url
Out[13]: 'http://forums.somethingawful.com/member.php?action=getinfo&userid=22993'

In [14]: profile = post.poster.url

In [15]: my_bad_post = "Dear Richard,"

In [16]: thread_id = bad_thread.id

In [17]: ap.session.reply(threadid, my_bad_post)


```

TODO

====



License
========

Modified GPLv3 w/ no commercial use w/o my consent + this clause must be applied to all derivatives.
