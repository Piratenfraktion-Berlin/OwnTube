from videoportal.models import Video
from videoportal.models import Comment
from videoportal.models import Channel
from django.contrib import admin

# Just a very stupid register, this should be nicer

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Channel)
