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

template_dir = os.path.join(os.path.dirname(__file__), '')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

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
        self.render("index.html")

    def post(self):
     	self.redirect('/do')

class DoHandler(Handler):
	def get(self):
		item = MenuItem(name="ItemName", food_category="Category", upvotes_prev=0, downvotes_prev=0,
						upvotes_today=0, downvotes_today=0)
		item.put()

		items = [item.key()]

		menu = Menu(breakfast=items)
		menu.put()

		self.response.out.write("DoHander Page")


class Menu(db.Model):
	date      = db.DateProperty()
	breakfast = db.ListProperty(db.Key)
	brunch    = db.ListProperty(db.Key)
	lunch     = db.ListProperty(db.Key)
	dinner    = db.ListProperty(db.Key)

class MenuItem(db.Model):
	name = db.StringProperty()
	food_category   = db.StringProperty()
	upvotes_prev    = db.IntegerProperty()
	downvotes_prev  = db.IntegerProperty()
	upvotes_today   = db.IntegerProperty()
	downvotes_today = db.IntegerProperty()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/do', DoHandler)
], debug=True)