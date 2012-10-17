from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from autoslug import AutoSlugField
from taggit.managers import TaggableManager

import appsettings as settings

from pytranscode.ffmpeg import *
from pytranscode.presets import *
from pytranscode.runner import *

import os
import subprocess
import re
import decimal 

import transmissionrpc
import urllib2
import datetime
import os
import shutil
import re
from threading import Event

from BitTorrent.btmakemetafile import calcsize, make_meta_file, ignore


KIND_CHOICES = (
    (0, 'Video-only'),
    (1, 'Audio-only'),
    (2, 'Audio & Video'),
)

class Video(models.Model):
    ''' The model for our videos. It uses slugs (with DjangoAutoSlug) and tags (with Taggit)
    everything else is quite standard. The sizes fields are used in the feeds to make enclosures
    possible. The videoThumbURL is the URL for Projekktor's "poster" and assemblyid is just a storage
    for the result we get back from transloadit so that we know which video just triggered the "encoding_done"
    view. Why are there URL fields and not file fields? Because you maybe want to use external storage
    (like Amazon S3) to store your files '''
    title = models.CharField(u"Titel",max_length=200)
    slug = AutoSlugField(populate_from='title',unique=True)
    date = models.DateField("Datum")
    description = models.TextField(u"Beschreibung")
    user = models.ForeignKey(User, blank=True, null=True)
    channel = models.ForeignKey('videoportal.Channel',blank=True,null=True)
    linkURL = models.URLField("Link",blank=True,verify_exists=False)
    kind = models.IntegerField("Art",max_length=1, choices=KIND_CHOICES)
    torrentURL = models.URLField("Torrent-URL",blank=True,verify_exists=False)
    mp4URL = models.URLField("MP4-URL",blank=True,verify_exists=False)
    mp4Size = models.BigIntegerField("MP4 Size in Bytes",null=True,blank=True)
    webmURL = models.URLField("WEBM-URL",blank=True,verify_exists=False)
    webmSize = models.BigIntegerField("WEBM Size in Bytes",null=True,blank=True)
    mp3URL = models.URLField("MP3-URL",blank=True,verify_exists=False)
    mp3Size = models.BigIntegerField("MP3 Size in Bytes",null=True,blank=True)
    oggURL = models.URLField("OGG-URL",blank=True,verify_exists=False)
    oggSize = models.BigIntegerField("OGG Size in Bytes",null=True,blank=True)
    videoThumbURL = models.URLField("Thumb-URL",blank=True,verify_exists=False)
    duration = models.DecimalField(null=True, max_digits=10, decimal_places=2,blank=True)
    autoPublish = models.BooleanField(default=True)
    published = models.BooleanField()
    encodingDone = models.BooleanField()
    torrentDone = models.BooleanField()
    assemblyid = models.CharField("Transloadit Result",max_length=100,blank=True)
    tags = TaggableManager("Tags")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    originalFile = models.FileField("Datei",upload_to="raw/%Y/%m/%d/",blank=True, max_length=2048)
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return "/videos/%s/" % self.slug
    def getClassName(self):
        return self.__class__.__name__

    def encode_media(self):
        ''' This is used to tell ffmpeg what to do '''
        kind = self.kind
        path = self.originalFile.path
        name_array = os.path.basename(self.originalFile.path).partition('.')
        name = slugify(name_array[0])
        outputdir = settings.ENCODING_OUTPUT_DIR + slugify(name)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        outputdir = outputdir + '/'
        if ((kind == 0) or (kind == 2)):
            logfile = settings.ENCODING_OUTPUT_DIR + 'encoding_mp4_log.txt'
            outfile_mp4 = outputdir + slugify(name) + '.mp4'
            # Create the command line
            cl_mp4 = ffmpeg(path, outfile_mp4, logfile, OWNTUBE_MP4_VIDEO, OWNTUBE_MP4_AUDIO).build_command_line()
            
            logfile = settings.ENCODING_OUTPUT_DIR + 'encoding_webm_log.txt'
            outfile_webm = outputdir + slugify(name) + '.webm'
    
            cl_webm = ffmpeg(path, outfile_webm, logfile, OWNTUBE_WEBM_VIDEO, OWNTUBE_WEBM_AUDIO).build_command_line()
            
            self.mp4URL = settings.ENCODING_VIDEO_BASE_URL + slugify(name) + '/' + slugify(name) + '.mp4'
            self.webmURL = settings.ENCODING_VIDEO_BASE_URL + slugify(name) + '/' + slugify(name) + '.webm' 
            self.videoThumbURL = settings.ENCODING_VIDEO_BASE_URL + slugify(name) + '/' + slugify(name) + '.jpg'
            outcode = subprocess.Popen(cl_mp4, shell=True)
            
            while outcode.poll() == None:
                pass
    
            if outcode.poll() == 0:
                self.mp4Size = os.path.getsize(outfile_mp4)
                self.duration = getLength(outfile_mp4)
            else:
                raise StandardError('Encoding MP4 Failed')
            
            print(cl_mp4)
            print(cl_webm)    
            outcode = subprocess.Popen(cl_webm, shell=True)
            
            while outcode.poll() == None:
                pass
    
            if outcode.poll() == 0:
                self.wembSize = os.path.getsize(outfile_webm)
            else:
                raise StandardError('Encoding WEBM Failed')
    
            outcode = subprocess.Popen(['ffmpeg -i '+ self.originalFile.path + ' -ss 5.0 -vframes 1 -f image2 ' + outputdir + slugify(name) + '.jpg'],shell = True)
            
            while outcode.poll() == None:
                pass
    
            if outcode.poll() == 0:
                pass 
            else:
                raise StandardError('Making Thumb Failed')
            
            
        if((kind == 1) or (kind == 2)):
            logfile = settings.ENCODING_OUTPUT_DIR + 'encoding_mp3_log.txt'
            outfile_mp3 = outputdir + slugify(name) + '.mp3'
            # Create the command line
            cl_mp3 = ffmpeg(path, outfile_mp3, logfile, OWNTUBE_NULL_VIDEO , OWNTUBE_MP3_AUDIO).build_command_line()
            
            logfile = settings.ENCODING_OUTPUT_DIR + 'encoding_ogg_log.txt'
            outfile_ogg = outputdir + slugify(name) + '.ogg'

            cl_ogg = ffmpeg(path, outfile_ogg, logfile, OWNTUBE_NULL_VIDEO, OWNTUBE_OGG_AUDIO).build_command_line()
            
            self.mp3URL = settings.ENCODING_VIDEO_BASE_URL + slugify(name) +  '/' + slugify(name) + '.mp3'
            self.oggURL = settings.ENCODING_VIDEO_BASE_URL + slugify(name) +  '/' + slugify(name) + '.ogg'
                        
            outcode = subprocess.Popen(cl_mp3, shell=True)
            
            while outcode.poll() == None:
                pass
    
            if outcode.poll() == 0:
                self.mp3Size = os.path.getsize(outfile_mp3)
                self.duration = getLength(outfile_mp3)
            else:
                raise StandardError('Encoding MP3 Failed')
                
            outcode = subprocess.Popen(cl_ogg, shell=True)
            
            while outcode.poll() == None:
                pass
    
            if outcode.poll() == 0:
                self.oggSize = os.path.getsize(outfile_ogg)
            else:
                raise StandardError('Encoding OGG Failed')
            
        self.encodingDone = True
        if settings.USE_BITTORRENT:
            self.torrentURL = settings.BITTORRENT_FILES_BASE_URL + self.slug + '.torrent'
            
        self.published = self.autoPublish
        self.save()
        
    def create_bittorrent(self):
        ''' This is where the bittorrent files are created and transmission is controlled'''
        flag = Event()
        make_meta_file(str(self.originalFile.path), settings.BITTORRENT_TRACKER_ANNOUNCE_URL, flag = flag, progress_percent=0, piece_len_exp = 18, target = settings.BITTORRENT_FILES_DIR + self.slug + '.torrent')
        self.torrentURL = settings.BITTORRENT_FILES_BASE_URL + self.slug + '.torrent'
        shutil.copy(str(self.originalFile.path), settings.BITTORRENT_DOWNLOADS_DIR)
        self.torrentDone = True
        self.published = self.autoPublish
        self.save()
        try:
            tc = transmissionrpc.Client(settings.TRANSMISSION_HOST, port=settings.TRANSMISSION_PORT)
            tc.add_uri(self.torrentURL, download_dir=settings.BITTORRENT_DOWNLOADS_DIR)
        except Exception, e:
            print "Error:", e
        
class Comment(models.Model):
    ''' The model for our comments, please note that (right now) OwnTube comments are moderated only'''
    name = models.CharField(u"Name",max_length=30)
    ip = models.IPAddressField("IP",blank=True,null=True)
    moderated = models.BooleanField()
    timecode = models.DecimalField(null=True, max_digits=10, decimal_places=2,blank=True)
    comment = models.TextField(u"Kommentar", max_length=1000)
    video = models.ForeignKey(Video)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.comment

class Channel(models.Model):
    ''' The model for our channels, all channels can hold videos but videos can only be part of one channel'''
    name = models.CharField(u"Name",max_length=30)
    slug = AutoSlugField(populate_from='name',unique=True)
    description = models.TextField(u"Beschreibung", max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    featured = models.BooleanField()
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/videos/channel/%s/" % self.slug

class Hotfolder(models.Model):
    ''' This is used for hotfolder support. Files in one of these will be added to owntube automagicly using a cron job and a manage task '''
    activated = models.BooleanField()
    channel = models.ForeignKey(Channel)
    folderName = models.CharField(u"Ordnername",max_length=30)
    defaultName = models.CharField(u"Standard Titel",max_length=30, blank=True)
    description = models.TextField(u"Standardbeschreibung", max_length=1000, null=True, blank=True)
    autoPublish = models.BooleanField(u"Automatisch Veroeffentlichen")
    kind = models.IntegerField("Art",max_length=1, choices=KIND_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.folderName

class Collection(models.Model):
    title = models.CharField(u"Titel", max_length=40)
    description = models.TextField(u"Beschreibung", max_length=1000)
    slug = AutoSlugField(populate_from='title',unique=True)
    date = models.DateField("Datum",null=True)
    videos = models.ManyToManyField('videoportal.Video')
    channel = models.ForeignKey('videoportal.Channel',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.title
    def getClassName(self):
        return self.__class__.__name__
    def get_absolute_url(self):
        return "/collection/%s/" % self.slug

def getLength(filename):
    ''' Just a little helper to get the duration (in seconds) from a video file using ffmpeg '''
    process = subprocess.Popen(['ffmpeg',  '-i', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
    duration = decimal.Decimal(matches['hours'])*3600 + decimal.Decimal(matches['minutes'])*60 + decimal.Decimal(matches['seconds'])
    return duration
