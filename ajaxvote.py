import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db

class Voting(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Voting page lol")

	def post(self):
		item_type = self.request.get('type')
		val = self.request.get('updatedvalue')
		item = self.request.get('menuitem').replace("\n", "").replace("\t", "")
		hall = self.request.get('dininghall')
		switched = self.request.get('switched')

		# Cookies
		votes = self.request.cookies.get('vote')
		self.response.headers.add_header('Set-Cookie', 'vote=%s&%s' % (str(votes), str(item).strip()))

		key = " " + item.strip() + " |" + hall.title()
		print key
		menu_item = memcache.get(key)

		if  menu_item:
			print "menu item here"
			if switched:
				print "switched lol"
				if item_type == "up":
					print "up here"
					#menu_item.downvotes_prev = menu_item.downvotes_prev - 1
					menu_item.upvotes_prev = menu_item.upvotes_prev + 1
				else:
					print "down here"
					menu_item.downvotes_prev = menu_item.downvotes_prev + 1
					#menu_item.upvotes_prev = menu_item.upvotes_prev - 1

			# Not switched
			else:
				print "not swtiched"
				if item_type == "up":
					print "up here"
					menu_item.upvotes_prev = menu_item.upvotes_prev + 1
				else:
					menu_item.downvotes_prev = menu_item.downvotes_prev + 1

			memcache.set(key, menu_item)
		else:
			print "else here"
			menu_item = db.get(key)
			menu_item.upvotes_prev = 1
			memcache.set(key, menu_item)

 

class Results(webapp2.RequestHandler):
	def get(self):
		cache = memcache.get(" French Fries |Hill")
		self.response.out.write(cache.upvotes_prev)