awful.py
=======

#### sa_tools
session, parsers and classes for forums, threads, posts, etc
works with python 2.7 and 3.4, probably everything in between as well.

##### awful_qml
py3k only, qtquick controls from qt 5.2, bad and broken.

![screenshot](http://i.imgur.com/R6odHSE.png "screenshot_of_app")


Usage
=======
## sa_tools

Scroll to the very bottom for instructions on how to post.

### Authenticating

```python
In [1]: from awful import AwfulPy
In [2]: ap = AwfulPy(username='username', passwd='passwd', save_session=False)
Loading from backup: .username_sa.bak
```

### Browse Sections

Flat index map

```python
In [26]: pprint(ap.index.forums)
{155: SA's Front Page Discussion,
 214: E/N Bullshit,
 1: GBS ,
 154: FYAD V,
 26: FYAD,
 48: Main,
 145: The MMO HMO,
 93: Private Game Servers,
 103: The Game Room,
 234: Traditional Games,
 191: Let's Play!,
 44: Games,
 192: Inspect Your Gadgets,
 162: Education & Academics,
 211: Tourism & Travel,
 200: Business, Finance, and Careers,
 158: Ask / Tell,
 46: Debate & Discussion,
 170: Haus of Tech Support,
 202: The Cavern of COBOL,
 219: YOSPOS,
 22: Serious Hardware / Software Crap,
 181: The Football Funhouse,
 248: The Armchair Quarterback,
 175: The Ray Parlour,
 177: Punchsport Pagoda,
 122: Sports Argument Stadium,
 183: The Goon Doctor,
 244: The Fitness Log Cabin,
 179: You Look Like Shit,
 161: Goons With Spoons,
 167: Post Your Favorite,
 236: Cycle Asylum,
 91: Automotive Insanity,
 124: Pet Island,
 132: The Firing Range,
 90: The Crackhead Clubhouse,
 218: Goons in Platoons,
 51: Discussion,
 210: DIY & Hobbies,
 247: The Dorkroom,
 31: Creative Convention,
 133: The Film Dump,
 151: Cinema Discusso,
 182: The Book Barn,
 104: Musician's Lounge,
 150: No Music Discussion,
 130: The TV IV,
 144: Batman's Shameful Secret,
 27: ADTRW,
 215: Entertainment, Weakly,
 152: The Finer Arts,
 77: Feedback & Discussion,
 85: Coupons & Deals,
 61: SA-Mart,
 43: Goon Meets,
 180: Stop, Collaborate, and Listen,
 241: LAN: Your City Sucks - Regional ,
 188: Questions, Comments, Suggestions,
 153: The Community,
 264: Comedy Purgatory,
 115: FYAD Goldmine,
 204: Helldump Success Stories,
 222: LF Goldmine,
 229: YCS Goldmine,
 21: Comedy Goldmine,
 25: Comedy Gas Chamber,
 49: Archives,
 -1: Index}


In [40]: forums = ap.index.forums
In [41]: the_pos = forums[219]
```

Hierarchical map

```python
In [37]: ap.index.sections
Out[37]: Index

In [29]: ap.index.sections.forums
Out[29]: [Main, Discussion, The Finer Arts, The Community, Archives]

In [47]: ap.index.sections.forums[1]
Out[47]: Discussion

In [48]: ap.index.sections.forums[1].children
Out[48]:
[Games,
 Inspect Your Gadgets,
 Ask / Tell,
 Debate & Discussion,
 Serious Hardware / Software Crap,
 Sports Argument Stadium,
 You Look Like Shit,
 Goons With Spoons,
 Post Your Favorite,
 Automotive Insanity,
 Pet Island,
 The Firing Range,
 The Crackhead Clubhouse,
 Goons in Platoons]

In [50]: ap.index.sections.forums[1].children[4]
Out[50]: Serious Hardware / Software Crap

In [51]: ap.index.sections.forums[1].children[4].children
Out[51]: [Haus of Tech Support, The Cavern of COBOL, YOSPOS]

In [52]: ap.index.sections.forums[1].children[4].children[2]
Out[52]: YOSPOS

In [53]: the_pos = ap.index.sections.forums[1].children[4].children[2]
```


### Forums and Navigation

If forum.unread is True, call forum.read(). Attribute access will trigger read() implicitly.

```python
In [59]: the_pos
Out[59]: YOSPOS


In [63]: the_pos.
the_pos.base_url  the_pos.name      the_pos.page      the_pos.parent    the_pos.session   the_pos.unread
the_pos.id        the_pos.navi      the_pos.pages     the_pos.read      the_pos.threads   the_pos.url

In [25]: the_pos.navi
Out[25]: Page 1 of 11

In [26]: the_pos.navi.
the_pos.navi.page     the_pos.navi.parent   the_pos.navi.session
the_pos.navi.pages    the_pos.navi.read     the_pos.navi.unread

In [64]: pprint(the_pos.threads)
{3522839: Your Operating System is a Piece of Shit: THE RULES,
 3617700: CJS: no butt stuff,
 3620430: You would all fuck your computers if they had an appropriate orifice for it,
 3617332: it's the new pics thread,
 3620724: it raining out =[,
 3201527: Description: that darn feline.jpg,
 3606857: Bitcoin: This is not funny. I feel violated.,
 3617986: Comptuer advertising: A hole, the entire content is the ad,
 3606828: Games: never pay more than $35.65 for a computer jame, sage advice from Tim Schafer,
 3620594: computers will never compete with this,
 3609208: YVCPOS II: George Lucas Jack-Me-Off Special edition,
 3561097: Post your idiot spare time projects.,
 3548182: terrible programmer safe zone/hideout,
 3620722: Little known fact about microchips,
 3610457: maul droppers, motorola and moonbounce: the yospos radio thread,
 3620716: I turned 32 today,
 3491370: it is the future and we need the yosposest cyberpunk names you got,
 3619802: the mac pro,
 3486712: post the most worthless kickstarters and greatest investor rewards you got,
 3481275: The PL (Programming Language) thread: I'm glad Python is the current hipste,
 3620250: what to tell your parents when they say their computer is running slow or h,
 3420578: sci fi postin,
 3568120: YOSPOS fitness thread,
 3607978: What the h*ck is happening to Microsoft?,
 3618779: we havent had a life hacks thread in a while so here's a life hack thread,
 3619547: Facebook releases new Virtual Reality Farmville games,
 3602746: Silicon Valley containment zone: Comedy Autopsy,
 3620315: g+. the greatest social network thing on the thing,
 3620450: I have an MBP and MPB,
 3620278: Security fuckup megathread v69 - nadim kobeissi is an idiot}
```

### Threads and LastRead

If thread.unread is True, call thread.read(). Attribute access will call read() implicitly.

```python
In [26]: random_thread = the_pos.threads.popitem()[-1]

In [27]: random_thread
Out[27]: monitor chat: "i don't care what i see as long as light is coming out"

In [28]: random_thread.read()

In [29]: random_thread.
random_thread.base_url   random_thread.last_read  random_thread.pages      random_thread.session    random_thread.user_id
random_thread.icon       random_thread.name       random_thread.parent     random_thread.title
random_thread.id         random_thread.navi       random_thread.posts      random_thread.unread
random_thread.lastpost   random_thread.page       random_thread.read       random_thread.url
```

Basic stats

```python
In [44]: random_thread.page
Out[44]: 1

In [45]: random_thread.pages
Out[45]: 8

In [46]: random_thread.lastpost
Out[46]: {'date': 'Mar 29, 2014', 'time': '00:50', 'user': 'pagancow'}

In [47]: random_thread.icon
Out[47]: 309

In [48]: random_thread.user_id
Out[48]: 105961

In [49]: random_thread.title
Out[49]: 'monitor chat: "i don\'t care what i see as long as light is coming out"'
```

Last read usage mixed in below

```python
In [31]: random_thread.last_read.
random_thread.last_read.id              random_thread.last_read.session         random_thread.last_read.unread_pages
random_thread.last_read.jump_to_new     random_thread.last_read.stop_tracking   random_thread.last_read.url_last_post
random_thread.last_read.parent          random_thread.last_read.unread          random_thread.last_read.url_switch_off
random_thread.last_read.read            random_thread.last_read.unread_count

In [31]: random_thread.last_read.__dict__
Out[31]:
{'id': 3616372,
 'parent': monitor chat: "i don't care what i see as long as light is coming out",
 'session': <requests.sessions.Session at 0x7f7ab5ba3d10>,
 'unread': False,
 'unread_count': 256,
 'unread_pages': 6,
 'url_last_post': 'http://forums.somethingawful.com//showthread.php?threadid=3616372&goto=newpost',
 'url_switch_off': 'http://forums.somethingawful.com//showthread.php?action=resetseen&threadid=3616372'}

In [27]: random_thread.page
Out[27]: 1

In [31]: random_thread.pages
Out[31]: 189

In [32]: random_thread.last_read.jump_to_new()

In [33]: random_thread.page
Out[33]: 97
```

```python
In [41]: pprint(random_thread.posts)
{427549842: Rufus Ping's reply: 427549842,
 427549895: OSI bean dip's reply: 427549895,
 427549966: USSMICHELLEBACHMAN's reply: 427549966,
 427549984: Install Windows's reply: 427549984,
 427550036: LARD LORD's reply: 427550036,
 427550042: Install Windows's reply: 427550042,
 427550069: USSMICHELLEBACHMAN's reply: 427550069,
 427550099: Rufus Ping's reply: 427550099,
 427550122: big scary monsters's reply: 427550122,
 427550208: double sulk's reply: 427550208,
 427550300: Install Windows's reply: 427550300,
 427550865: Ab Fablet's reply: 427550865,
 427552380: Wiggly Wayne DDS's reply: 427552380,
 427553150: Displeased Moo Cow's reply: 427553150,
 427553250: power botton's reply: 427553250,
 427553456: Displeased Moo Cow's reply: 427553456,
 427553590: compuserved's reply: 427553590,
 427553597: Miley Virus's reply: 427553597,
 427553656: Chris Knight's reply: 427553656,
 427553773: big scary monsters's reply: 427553773,
 427553980: Rufus Ping's reply: 427553980,
 427554244: eithedog's reply: 427554244,
 427555357: jony ive aces's reply: 427555357,
 427555384: Nelson MandEULA's reply: 427555384,
 427556249: cheese-cube's reply: 427556249,
 427556376: cheese-cube's reply: 427556376,
 427556959: PuTTY riot's reply: 427556959,
 427556989: Nelson MandEULA's reply: 427556989,
 427557002: Nelson MandEULA's reply: 427557002,
 427557159: cheese-cube's reply: 427557159,
 427558303: Lightbulb Out's reply: 427558303,
 427558937: cheese-cube's reply: 427558937,
 427559011: OSI bean dip's reply: 427559011,
 427559016: graph's reply: 427559016,
 427559078: Werthog 95's reply: 427559078,
 427559138: OSI bean dip's reply: 427559138,
 427559169: Sniep's reply: 427559169,
 427559181: jony ive aces's reply: 427559181,
 427559194: Werthog 95's reply: 427559194,
 427559680: Rufus Ping's reply: 427559680}
```

### Posts and Posters

```python
In [72]: bad_post = random_thread.posts.popitem()[-1]

In [74]: bad_post.body
Out[74]: 'I.N.R.I posted:\r\ndont even bother asking then moron.\n\n\r\nkeep the curse words to yourself please, are you not in the usa or something'

In [75]: bad_post.id
Out[75]: 421953760

In [76]: bad_post.poster
Out[76]: vaginal culture
```

```python
In [59]: bad_poster = bad_post.poster

In [60]: bad_poster
Out[60]: echinopsis

In [61]: bad_poster.id
Out[61]: 52833

In [62]: bad_poster.name
Out[62]: 'echinopsis'

In [63]: bad_poster.url
Out[63]: 'https://forums.somethingawful.com/member.php?action=getinfo&userid=52833'
```


### Posting and Sessions

```python
In [11]: random_thread
Out[11]: YOSPOS fitness thread

In [12]: session = ap.session
In [13]: post_body = "Wow"

In [14]: session.reply(random_thread.id, post_body)

In [15]: random_thread.page
Out[15]: 1

In [16]: random_thread.read(random_thread.pages)

In [17]: random_thread.page
Out[17]: 189

In [19]: last_post = random_thread.posts.popitem(-1)
In [23]: last_post
Out[23]: salisbury shake's reply: 427594324

In [24]: last_post.body
Out[24]: 'Wow'

In [25]: last_post.id
Out[25]: 427594324

In [26]: last_post.poster
Out[26]: salisbury shake

In [30]: last_post.poster.id
Out[30]: 182905
```


License
========

GPLv3
