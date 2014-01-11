AwfulPy
=======

#### SATools
forums session, methods, and scraper. 
works with python 2.7 and 3.3, probably everything in between as well. 

##### AwfulQML
preliminary gui to SATools. this is not ready for any kind of use. py3k only.

![screenshot](http://i.imgur.com/PhZrAzU.png "threads_view")

don't get this banned. thanks.

Usage
=======


## SATools

### Authenticating

```python
from AwfulPy import AwfulPy
ap = AwfulPy('username', 'passwd')
```

Pass `save_session=False` if you'd rather not save cookies to disk. If your session is saved you only need to pass your username to AwfulPy

```python
In [1]: from AwfulPy import AwfulPy
In [2]: username, passwd, not_paranoid = 'your_username', 'your_passwd', False
In [3]: ap = AwfulPy(username, passwd, save_session=not_paranoid)
Loading from backup: .salisbury shake_sa.bak

```

### Navigating Index

```python
gbs = ap.index.forums['1']
```

the AwfulPy object has members `index` and `session`. the former is used to navigate the forum, the latter has the relevant methods to do so. `reply()` is a method of the `session` object.

`listing` threadid: thread_title map provides a readable output of a section or forum. use the key from the listings to retrieve the `SAForum` object from the `forums` attribute. we can also walk down the `sections` map if you like hierarchy.

to save time and battery life, `read()` will pull and parse the forums data. if `listings` is empty, call `read()`.

Here we navigate the forum index, and select a forum.


```python
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
```

### Navigating Forum

```python
cat_thread = ap.index.forums['219'].threads['3136320']
```

call `read()` to pull and parse the forum's data.

`listings` provides a human readable index for the `threads` map of `SAThread`s

Here we select a thread.


```python
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
```

### Navigating thread

```python 
dont_fuck_with = [post for post in cat_thread if post.poster.name == 'Debt']
```

call `read()` to parse the thread's posts and op's metadata. 

We can see the different attributes the `SAThread` object has after being read.

Here we iterate over the `posts` map of `SAPost` objects.


```python
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
```

### Post and Poster objects

```python
take_a_better_look_at = post.date, post.poster.reg_date

```

if a post was generated from a `SAThread` that's been read, there is no reason to call `read()` if attributes are missing, you may call it, but it will pull info from the poster's profile url. best option is to just display what's been given to the object unless an individual poster needs to be inspected.

```python
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
```

### Posting
The `SASession` object at `AwfulPy.session` holds methods that need to be invoked with your credentials.
`reply()` lives here and so will `post_thread()`, `pms`, and `search()` eventually. 

`reply()` requires an existing threadid to reply to and a message to be posted. an exception will be raised if it didn't work


```python
In [15]: my_bad_post = "Dear Richard,"
In [16]: thread_id = bad_thread.id
In [17]: ap.session.reply(threadid, my_bad_post)


```

TODO
====
+ provide qobject intermediates for satools objects
+ provide qml models/views for qobjects
+ clean up SATools. if you want to contribute, look here first. code is simple but bad.



License
========

Modified GPLv3 w/ no commercial use w/o my consent + this clause must be applied to all derivatives.
