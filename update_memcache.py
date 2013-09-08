from google.appengine.api import memcache
from google.appengine.ext import db
import webapp2
import datetime
from crawler_gae import crawl
import main

class Update_Cache(webapp2.RequestHandler):
	def get(self):
		update()

		
def update():
	date_today = datetime.date.today()
	date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)

	commons_today = db.GqlQuery("SELECT * FROM Menu WHERE date=:date_today AND hall_name=:hall", date_today=date_today, hall="Commons")
	hill_today    = db.GqlQuery("SELECT * FROM Menu WHERE date=:date_today AND hall_name=:hall", date_today=date_today, hall="Hill")
	kc_today      = db.GqlQuery("SELECT * FROM Menu WHERE date=:date_today AND hall_name=:hall", date_today=date_today, hall="KC")

	commons_tomorrow = db.GqlQuery("SELECT * FROM Menu WHERE date=:date_today AND hall_name=:hall", date_today=date_tomorrow, hall="Commons")
	hill_tomorrow    = db.GqlQuery("SELECT * FROM Menu WHERE date=:date_today AND hall_name=:hall", date_today=date_tomorrow, hall="Hill")
	kc_tomorrow      = db.GqlQuery("SELECT * FROM Menu WHERE date=:date_today AND hall_name=:hall", date_today=date_tomorrow, hall="KC")

	commons_today = main.menu_list(list(commons_today)[0])
	hill_today = main.menu_list(list(hill_today)[0])
	kc_today = main.menu_list(list(kc_today)[0])

	commons_tomorrow = main.menu_list(list(commons_tomorrow)[0])
	hill_tomorrow = main.menu_list(list(hill_tomorrow)[0])
	kc_tomorrow = main.menu_list(list(kc_tomorrow)[0])

	memcache.set("today|commons", commons_today)
	memcache.set("today|hill", hill_today)
	memcache.set("today|kc", kc_today)
	memcache.set("tomorrow|commons", commons_tomorrow)
	memcache.set("tomorrow|hill", hill_tomorrow)
	memcache.set("tomorrow|kc", kc_tomorrow)