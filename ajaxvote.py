import webapp2
from google.appengine.api import memcache

class Voting(webapp2.RequestHandler):
	def get(self):
		item_type = self.request.get('type')
		val = self.request.get('updatedvalue')
		item = self.request.get('menuitem')
		hall = self.request.get('dininghall')
		switched = self.request.get('switched')

		if item:
			memcache.set("vote", item)

		cache_item = memcache.get("vote")
		self.response.out.write(cache_item)