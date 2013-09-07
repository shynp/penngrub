from bs4 import BeautifulSoup
import urllib2

url_commons_weekly = "http://cms.business-services.upenn.edu/dining/hours-locations-a-menus/residential-dining/1920-commons/weekly-menu.html"
url_hill_weekly    = "http://cms.business-services.upenn.edu/dining/hours-locations-a-menus/residential-dining/hill-house/weekly-menu.html"
url_kc_weekly      = "http://cms.business-services.upenn.edu/dining/hours-locations-a-menus/residential-dining/kings-court-english-house/weekly-menu.html"

commons_weekly_content = urllib2.urlopen(url_commons_weekly).read()
hill_weekly_content    = urllib2.urlopen(url_hill_weekly).read()
kc_weekly_content      = urllib2.urlopen(url_kc_weekly).read()
