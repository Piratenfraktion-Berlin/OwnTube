from django.contrib.syndication.views import Feed
from videoportal.models import Video

import appsettings as settings

import os

class LatestMP4Videos(Feed):
    ''' This class (like the following) are handling the feed requests from urls.py.
    TODO:
    Better handling: We sould only use one Feed class and get the desired format with GET
    Dynamic Title for the Feed''' 
    title = "OwnTube Latest Videos"
    link = "/"
    description = "The newest media from OwnCloud"
    item_enclosure_mime_type = "video/mp4"
	
    def items(self):
        return Video.objects.filter(published=True).exclude(mp4URL='').order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
        
    def item_enclosure_url(self, item):
    	return item.mp4URL
    	
    def item_enclosure_length(self, item):
    	return item.mp4Size
    	
    def item_pubdate(self, item):
    	return item.created
    	
class LatestWEBMVideos(Feed):
    title = "OwnTube Latest Videos"
    link = "/"
    description = "The newest media from OwnCloud"
    item_enclosure_mime_type = "video/webm"
	
    def items(self):
        return Video.objects.filter(published=True).exclude(webmURL='').order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
        
    def item_enclosure_url(self, item):
    	return item.webmURL
    	
    def item_enclosure_length(self, item):
    	return item.webmSize
    	
    def item_pubdate(self, item):
    	return item.created
    	
class LatestMP3Audio(Feed):
    title = "OwnTube Latest Audio Files"
    link = "/"
    description = "The newest media from OwnCloud"
    item_enclosure_mime_type = "video/webm"
	
    def items(self):
        return Video.objects.filter(published=True).exclude(mp3URL='').order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
        
    def item_enclosure_url(self, item):
    	return item.mp3URL
    	
    def item_enclosure_length(self, item):
    	return item.mp3Size
    	
    def item_pubdate(self, item):
    	return item.created
    	
class LatestOGGAudio(Feed):
    title = "OwnTube Latest Audio Files"
    link = "/"
    description = "The newest media from OwnCloud"
    item_enclosure_mime_type = "video/webm"
	
    def items(self):
        return Video.objects.filter(published=True).exclude(oggURL='').order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
        
    def item_enclosure_url(self, item):
    	return item.oggURL
    	
    def item_enclosure_length(self, item):
    	return item.oggSize
    	
    def item_pubdate(self, item):
    	return item.created

class TorrentFeed(Feed):
    title = "OwnTube TorrentFeed"
    link = "/"
    description = "Torrent files from OwnTube"
    item_enclosure_mime_type = "application/x-bittorrent"
	
    def items(self):
        return Video.objects.filter(published=True).exclude(torrentURL='').order_by('-created')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
        
    def item_enclosure_url(self, item):
    	return item.torrentURL
    	
    def item_enclosure_length(self, item):
    	return os.path.getsize(settings.BITTORRENT_FILES_DIR + item.slug + '.torrent')
    	
    def item_pubdate(self, item):
    	return item.created