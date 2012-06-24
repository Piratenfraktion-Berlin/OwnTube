from django.db import models
from django.utils.safestring import mark_safe 

from autoslug import AutoSlugField

# Create your models here.

class Stream(models.Model):
    ''' This is the model for each live stream event nothing really special
    except for the iframe field maybe. It contains the loaded iframe for 
    each stream event and is marked as safe. Maybe we change this or add
    support for streams directly loaded into Projekktor'''
    title = models.CharField("Stream-Titel",max_length=200)
    slug = AutoSlugField(populate_from='title',unique=True)
    startDate = models.DateTimeField("Start der Veranstaltung")
    endDate = models.DateTimeField("Ende der Veranstaltung")
    description = models.TextField("Beschreibung")
    link = models.URLField("Link",blank=True,verify_exists=False)
    rtmpLink = models.URLField("RTMP Link",blank=True,verify_exists=False)
    audioOnlyLink = models.URLField("Audio-only Link",blank=True,verify_exists=False)
    iframe = models.TextField("iFrame des Streams")
    published = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/stream/%s/" % self.slug
    def display_iFrameSafeField(self): 
        return mark_safe(self.iframe)