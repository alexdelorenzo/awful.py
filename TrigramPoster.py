
from SATools.SASearch import SASearch
from SATools.SAPoster import SAPoster

from time import sleep
import nltk

class TrigramPoster(SAPoster):
	def __init__(self, id, session, **options):
		super().__init__(id=id, session=session, **options)
		self.search = SASearch(query=self.id,
		                       type='user',
		                       session=self.session)

		self.search.search_profile(self)
		self.model = None

	def create_model(self, pgs=1, posts=None, start=1):
		if not posts:
			posts = self._create_list_of_posts(start, pgs)

		self.model = self._ngramify(self._tokenize(posts))

	def _create_list_of_posts(self, start=1, pgs=1, time=.25):
		pages = range(start, pgs+1)
		posts = []
		for page in pages:
			self.search.read(pg=page)

			for result in self.search.results:
				result.get_post()
				posts.append(result.post.body)
				print(result.url)
				sleep(time) # let's not get banned

		posts = ' '.join(posts)
		return posts

	def _tokenize(self, posts):
		return nltk.tokenize.word_tokenize(posts)

	def _ngramify(self, tokenized):
		return nltk.NgramModel(3, tokenized)
