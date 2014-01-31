
from SATools.SASearch import SASearch
from SATools.SAPoster import SAPoster
import nltk

class TrigramPoster(SAPoster):
	def __init__(self, id, session, **options):
		super().__init__(id=id, session=session, **options)
		self.search = SASearch(query=self.id,
		                       type='user',
		                       session=self.session)

		self.search.search_profile(self)
		self.model = None

	def create_model(self, pgs=1):
		posts = self._create_list_of_posts(pgs)
		self.model = self.ngramify(self.tokenize(posts))

	def _create_list_of_posts(self, pgs=1):
		pages = range(1, pgs+1)
		posts = []
		for page in pages:
			self.search.read(pg=page)

			for result in self.search.results:
				result.get_post()
				posts.append(result.post.body)

		return posts

	def tokenize(self, post_list):
		posts = ' '.join(post_list)
		return nltk.tokenize.word_tokenize(posts)

	def ngramify(self, tokenized):
		return nltk.NgramModel(3, tokenized)
