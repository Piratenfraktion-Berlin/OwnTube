from django.contrib.syndication.views import Feed
from livestream.models import Stream

import datetime

class UpcomingEvents(Feed):
''' This sub class of Django's Feed class handles the feed URL from urls.py
    in the owntube directory, it gets all upcoming
    streaming events and returns the data as required
    for the django feed class
    TO DO: 
    Making it possible to change the title and so on in a better way,
    maybe in the admin app?
    '''
    title = "Die kommenden Streams"
    link = "/stream/"
    description = "Hier kommen die Streams an"
	
    def items(self):
        return Stream.objects.filter(published=True,endDate__gt=datetime.datetime.now).order_by('-startDate')

    def item_title(self, item):
        return str(item.startDate) + ' ' + item.title

    def item_description(self, item):
        return item.description
    	
    def item_pubdate(self, item):
    	return item.created
