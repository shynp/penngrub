from bs4 import BeautifulSoup
import urllib2
import webapp2
from google.appengine.ext import db
import unicodedata

url_commons_weekly = "http://cms.business-services.upenn.edu/dining/hours-locations-a-menus/residential-dining/1920-commons/weekly-menu.html"
url_hill_weekly    = "http://cms.business-services.upenn.edu/dining/hours-locations-a-menus/residential-dining/hill-house/weekly-menu.html"
url_kc_weekly      = "http://cms.business-services.upenn.edu/dining/hours-locations-a-menus/residential-dining/kings-court-english-house/weekly-menu.html"

commons_weekly_content = urllib2.urlopen(url_commons_weekly).read()
hill_weekly_content    = urllib2.urlopen(url_hill_weekly).read()
kc_weekly_content      = urllib2.urlopen(url_kc_weekly).read()

soup_commons = BeautifulSoup(commons_weekly_content)
soup_hill    = BeautifulSoup(hill_weekly_content)
soup_kc      = BeautifulSoup(kc_weekly_content)

halls = [soup_commons, soup_hill, soup_kc]

def crawl():

	# Get all menu_items from DB
	#db_menu_items = db.GqlQuery("SELECT * FROM MenuItem")
	#db_menu_items = list(db_menu_items)

	global soup_commons
	halls = [soup_commons]

	for hall in halls:
		hall_name = None
		if hall == soup_commons:
			hall_name = "Commons"
		elif hall == soup_hill:
			hall_name = "Hill"
		elif hall == soup_kc:
			hall_name = "KC" 


		# Checks for hall_name is valid
		if hall_name == None:
			print "Error: hall_name is None"
			break

		dates = hall.findAll("h2")
		for date in dates:

			meals = date.next_sibling.findAll("h4")
			for meal in meals:
				meal_categories = meal.next_sibling.findAll("strong")

				for meal_category in meal_categories:		

					menu_items = meal_category.next_sibling.next.findAll("li")
					for menu_item in menu_items:
						menu_item_str = unicode(menu_item.next).encode('ascii', 'ignore')
						print type(menu_item_str)
						db_item = MenuItem(key_name=menu_item_str, food_category=str(meal_category.next.next), upvotes_prev=0, upvotes_today=0, downvotes_prev=0, downvotes_today=0)
						db_item.put()
					

class CrawlerHandler(webapp2.RequestHandler):
	def get(self):
		crawl()
		self.response.out.write("Crawler Page")

class Menu(db.Model):
	hall_name = db.StringProperty()
	date      = db.DateProperty()
	breakfast = db.ListProperty(db.Key)
	brunch    = db.ListProperty(db.Key)
	lunch     = db.ListProperty(db.Key)
	dinner    = db.ListProperty(db.Key)

class MenuItem(db.Model):
	food_category   = db.StringProperty()
	upvotes_prev    = db.IntegerProperty()
	downvotes_prev  = db.IntegerProperty()
	upvotes_today   = db.IntegerProperty()
	downvotes_today = db.IntegerProperty()
