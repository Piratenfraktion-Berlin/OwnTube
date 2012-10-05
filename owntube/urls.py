from django.conf.urls import patterns, include, url
from videoportal.feeds import *
from livestream.feeds import UpcomingEvents
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'videoportal.views.list'),
    url(r'^videos/(?P<slug>[-\w]+)/$', 'videoportal.views.detail'),
    url(r'^tags/(?P<tag>[-\w]+)/$', 'videoportal.views.tag'),
    url(r'^json_tags/(?P<tag>[-\w]+)/$', 'videoportal.views.tag_json'),
    url(r'^videos/channel/(?P<slug>[-\w]+)/$', 'videoportal.views.channel_list'),
    url(r'^videos/iframe/(?P<slug>[-\w]+)/$', 'videoportal.views.iframe'),
    url(r'^search/', 'videoportal.views.search'),
    url(r'^json_search/', 'videoportal.views.search_json'),
    url(r'^submit/', 'videoportal.views.submit'),
    url(r'^encodingdone/', 'videoportal.views.encodingdone'),
    url(r'^contact/', 'static_pages.views.contact'),
    url(r'^about/', 'static_pages.views.about'),
    url(r'^stream/$', 'livestream.views.current'),
    url(r'^stream/list/$', 'livestream.views.list'),
    url(r'^stream/(?P<slug>[-\w]+)/$', 'livestream.views.detail'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^feeds/latest/mp4', LatestMP4Videos()),
    url(r'^feeds/latest/webm', LatestWEBMVideos()),
    url(r'^feeds/latest/mp3', LatestMP3Audio()),
    url(r'^feeds/latest/ogg', LatestOGGAudio()),
    url(r'^feeds/stream/upcoming', UpcomingEvents()),
    url(r'^feeds/latest/torrent', TorrentFeed()),
    url(r'^feeds/(?P<channel_slug>[-\w]+)/mp4/$', ChannelFeedMP4()),
    url(r'^feeds/(?P<channel_slug>[-\w]+)/webm/$', ChannelFeedWEBM()),
    url(r'^feeds/(?P<channel_slug>[-\w]+)/ogg/$', ChannelFeedOGG()),
    url(r'^feeds/(?P<channel_slug>[-\w]+)/mp3/$', ChannelFeedMP3()),
    url(r'^feeds/(?P<channel_slug>[-\w]+)/torrent/$', ChannelFeedTorrent()),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
