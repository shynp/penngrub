from google.appengine.api import memcache
from google.appengine.ext import db
import webapp2
import datetime
import main

class Update_Cache(webapp2.RequestHandler):
	def get(self):
		update()

		
def update():
	date_today = datetime.date.today() - datetime.timedelta(days=2)
	date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)

	query_today = db.GqlQuery("SELECT * FROM Menu WHERE date=:1", date_today)
	query_today = list(query_today)

	query_tomorrow = db.GqlQuery("SELECT * FROM Menu WHERE date=:1", date_tomorrow)
	query_tomorrow = list(query_tomorrow)

	commons_today    = None
	hill_today       = None
	kc_today         = None
	commons_tomorrow = None
	hill_tomorrow    = None
	kc_tomorrow      = None

	for menu in query_today:
		if menu.hall_name == "Commons":
			commons_today = main.menu_list(menu)
		elif menu.hall_name == "Hill":
			hill_today = main.menu_list(menu)
		elif menu.hall_name == "KC":
			kc_today = main.menu_list(menu)

	for menu in query_tomorrow:
		if menu.hall_name == "Commons":
			commons_tomorrow = main.menu_list(menu)
		elif menu.hall_name == "Hill":
			hill_tomorrow = main.menu_list(menu)
		elif menu.hall_name == "KC":
			kc_tomorrow = main.menu_list(menu)


	memcache.set("today|commons", commons_today)
	memcache.set("today|hill", hill_today)
	memcache.set("today|kc", kc_today)
	memcache.set("tomorrow|commons", commons_tomorrow)
	memcache.set("tomorrow|hill", hill_tomorrow)
	memcache.set("tomorrow|kc", kc_tomorrow)