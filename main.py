#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.ext import db
import crawler_gae
from google.appengine.api import memcache
import datetime

import update_memcache
import ajaxvote

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def menu_list(menu):
	menu_l = []
	if menu.breakfast:
		menu_l.append(keys_to_models(menu.breakfast))
	if menu.brunch:
		menu_l.append(keys_to_models(menu.brunch))
	if menu.lunch:
		menu_l.append(keys_to_models(menu.lunch))
	if menu.dinner:
		menu_l.append(keys_to_models(menu.dinner))

	return menu_l

def keys_to_models(keys):
	if len(keys) == 0:
		return

	models = []
	for key in keys:
		models.append(db.get(key))

	return models

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
    	commons_today = memcache.get("today|commons")
    	hill_today    = memcache.get("today|hill")
    	kc_today      = memcache.get("today|kc")

    	if commons_today or hill_today or kc_today:
    		self.render("index.html", commons=commons_today, hill=hill_today, kc=kc_today)

    	else:
    		"""date_today = datetime.date.today()
    		date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    		menus = db.GqlQuery("SELECT * FROM Menu WHERE date=:1", date_today)
    		menus = list(menus)

    		commons = None
    		hill = None
    		kc = None

    		for menu in menus:
    			if menu.hall_name == "Commons":
    				commons = menu_list(menu)
    			elif menu.hall_name == "Hill":
    				hill = menu_list(menu)
    			elif menu.hall_name == "KC":
    				kc = menu_list(menu)
    		
    		if commons != None:
    			memcache.set("today|commons", commons)
    		if hill != None:	
    			memcache.set("today|hill", hill)
    		if kc != None:
    			memcache.set("today|kc", kc)"""

    		update_memcache.update()
    		commons_today = memcache.get("today|commons")
    		hill_today    = memcache.get("today|hill")
    		kc_today      = memcache.get("today|kc")
    		self.render("index.html", commons=commons_today, hill=hill_today, kc=kc_today)

    def post(self):
     	self.redirect('/do')

class DoHandler(Handler):
	def get(self):
		self.response.out.write("DoHander Page")

class DeleteDB(Handler):
	def get(self):
		db.delete(MenuItem.all())
		db.delete(Menu.all())
		self.response.out.write("DeleteDB")


class Menu(db.Model):
	hall_name = db.StringProperty()
	date      = db.DateProperty()
	breakfast = db.ListProperty(db.Key)
	brunch    = db.ListProperty(db.Key)
	lunch     = db.ListProperty(db.Key)
	dinner    = db.ListProperty(db.Key)

class MenuItem(db.Model):
	name            = db.StringProperty()
	description     = db.StringProperty()
	food_category   = db.StringProperty()
	hall_name       = db.StringProperty()
	upvotes_prev    = db.IntegerProperty()
	downvotes_prev  = db.IntegerProperty()
	upvotes_today   = db.IntegerProperty()
	downvotes_today = db.IntegerProperty()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/do', DoHandler),
    ('/crawler', crawler_gae.CrawlerHandler),
    ('/delete', DeleteDB),
    ('/update', update_memcache.Update_Cache),
    ('/vote', ajaxvote.Voting),
    ('/result', ajaxvote.Results)
], debug=True)