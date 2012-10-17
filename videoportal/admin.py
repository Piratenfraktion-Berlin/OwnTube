from videoportal.models import Video
from videoportal.models import Comment
from videoportal.models import Channel
from videoportal.models import Hotfolder
from videoportal.models import Collection

from django.contrib import admin

def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Markierte Videos veroeffentlichen"

def make_torrent_done(modeladmin, request, queryset):
    queryset.update(torrentDone=True)
make_published.short_description = "Markierte Videos also mit Torrent markieren"

class VideoAdmin (admin.ModelAdmin):
    list_display = ['title','published','encodingDone', 'channel' ,'date']
    ordering = ['-date','-created']
    actions = [make_published,make_torrent_done]

admin.site.register(Video,VideoAdmin)

def make_moderated(modeladmin,request, queryset):
    queryset.update(moderated=True)
make_moderated.short_description = "Markierte Kommentare zulassen"

class CommentAdmin (admin.ModelAdmin):
    list_display = ['comment','video','created','name','ip','moderated']
    ordering = ['-created']
    actions = [make_moderated]

admin.site.register(Comment,CommentAdmin)

class ChannelAdmin (admin.ModelAdmin):
    list_display = ['name','description','featured']
    ordering = ['-created']

admin.site.register(Channel,ChannelAdmin)

class HotfolderAdmin (admin.ModelAdmin):
    list_display = ['folderName','activated','autoPublish','kind','channel']
    ordering = ['-created']

admin.site.register(Hotfolder,HotfolderAdmin)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','date','channel']
    ordering = ['-date','-created']

admin.site.register(Collection,CollectionAdmin)
