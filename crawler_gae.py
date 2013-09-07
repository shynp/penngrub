from bs4 import BeautifulSoup
import urllib2
import webapp2
from google.appengine.ext import db
import main
import re
from google.appengine.api import memcache
from datetime import datetime

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
			date_db = datetime.strptime(date.next,'%m/%d/%Y').date()
			db_menu = main.Menu(hall_name=hall_name, date=date_db)

			meals = date.next_sibling.findAll("h4")
			for meal in meals:
				meal_categories = meal.next_sibling.findAll("strong")

				for meal_category in meal_categories:
					menu_items = meal_category.next_sibling.next.findAll("li")

					for menu_item in menu_items:
						menu_split = re.split(r"\(|-", menu_item.next, 1)

						menu_item_name = menu_split[0].replace("\n", "").title()

						# Get menu_item_descr if it exists
						if len(menu_split) == 2:
							menu_item_desc = menu_split[1].replace("\n", "")
						else:
							menu_item_desc = "No description."

						# Add menu_item to memcache and database if not already there
						if not memcache.get(menu_item_name):
							db_item = main.MenuItem(key_name=menu_item_name, name=menu_item_name, description=menu_item_desc, food_category=str(meal_category.next.next), 
													upvotes_prev=0, upvotes_today=0, downvotes_prev=0, downvotes_today=0)

							meal_name = meal.next
							if meal_name == "LUNCH":
								db_menu.lunch.append(db_item.key())
							elif meal_name == "BREAKFAST":
								db_menu.breakfast.append(db_item.key())
							elif meal_name == "BRUNCH":
								db_menu.brunch.append(db_item.key())
							elif meal_name == "DINNER":
								db_menu.dinner.append(db_item.key())

							db_item.put()
							memcache.set(menu_item_name, db_item)


			db_menu.put()


def print_db():
	db_menu_items = db.GqlQuery("SELECT * FROM MenuItem")
	db_menu_items = list(db_menu_items)
	print type(db_menu_items)
	print dir(db_menu_items)

	print type(db_menu_items[0])
	print dir(db_menu_items[0])
	print db_menu_items[0].key().name()
					

class CrawlerHandler(webapp2.RequestHandler):
	def get(self):
		crawl()
		self.response.out.write("Crawler Page")
