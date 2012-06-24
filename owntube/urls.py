from django.conf.urls import patterns, include, url
from videoportal.feeds import LatestMP4Videos, LatestWEBMVideos, LatestMP3Audio, LatestOGGAudio, TorrentFeed
from livestream.feeds import UpcomingEvents
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'videoportal.views.list'),
    url(r'^videos/(?P<slug>[-\w]+)/$', 'videoportal.views.detail'),
	url(r'^tags/(?P<tag>[-\w]+)/$', 'videoportal.views.tag'),
	url(r'^search/', 'videoportal.views.search'),
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

    # url(r'^owntube/', include('owntube.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
