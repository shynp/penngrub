from bs4 import BeautifulSoup
import urllib2

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

dates = soup_commons.findAll("h2")

# Breakfast, Lunch, Dinner, Brunch nodes 
meals = dates[0].next_sibling.findAll("h4")

# Meal categories
meal_categories = meals[0].next_sibling.findAll("strong")

# Menu items
menu_items = meal_categories[0].next_sibling.next.findAll("li")

# Individual item
menu_single = menu_items[0].next

# Item name
(menu_name, menu_desc) = menu_single.split('(')

######

# hall_name 
# date

db_data = {}

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
		#print hall_name + " on " + date.next

		meals = date.next_sibling.findAll("h4")
		for meal in meals:
			#print "For " + meal.next
			meal_categories = meal.next_sibling.findAll("strong")

			for meal_category in meal_categories:
				#print "--" + meal_category.next.next

				menu_items = meal_category.next_sibling.next.findAll("li")
				for menu_item in menu_items:
					#print "---" + menu_item.next

					db_data[menu_item.next] = [menu_item.next, meal_category.next.next, meal.next, date.next, hall_name]

for val in db_data.itervalues():
	print val	