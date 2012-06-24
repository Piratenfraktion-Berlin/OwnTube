from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.list_detail import object_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from videoportal.models import Video, Comment
from videoportal.forms import VideoForm, CommentForm
from transloadit.client import Client

import appsettings as settings

from BitTorrent.btmakemetafile import calcsize, make_meta_file, ignore

import djangotasks

import simplejson as json
import transmissionrpc
import urllib2
import datetime
import os
import shutil
import re
from threading import Event
from traceback import print_exc
from sys import argv

def list(request):
    latest_videos_list = Video.objects.filter(encodingDone=True).order_by('-date')
    paginator = Paginator(latest_videos_list,15)
    
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)
    return render_to_response('videos/index.html', {'latest_videos_list': videos},
                            context_instance=RequestContext(request))


def detail(request, slug):
    if request.method == 'POST':
            comment = Comment(video=Video.objects.get(slug=slug),ip=request.META["REMOTE_ADDR"])
            video = get_object_or_404(Video, slug=slug)
            emptyform = CommentForm()
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                    comment = form.save(commit=False)
                    comment.save()
                    comments = Comment.objects.filter(moderated=True, video=video).order_by('-created')
                    message = "Ihr Kommentar muss noch freigeschaltet werden"
            
            return render_to_response('videos/detail.html', {'video': video, 'comment_form': emptyform, 'comments': comments, 'message': message}, context_instance=RequestContext(request))
                    
    else:
        video = get_object_or_404(Video, slug=slug)
        form = CommentForm()
        comments = Comment.objects.filter(moderated=True, video=video).order_by('-created')
        return render_to_response('videos/detail.html', {'video': video, 'comment_form': form, 'comments': comments},
                            context_instance=RequestContext(request))
def tag(request, tag):
    videolist = Video.objects.filter(encodingDone=True, tags__name__in=[tag]).order_by('-date')
    return render_to_response('videos/list.html', {'videos_list': videolist, 'tag':tag},
                            context_instance=RequestContext(request))
                            
def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        entry_query = get_query(query_string, ['title', 'description',])
        
        found_entries = Video.objects.filter(entry_query).order_by('-date')

    return render_to_response('videos/search_results.html',
                          { 'query_string': query_string, 'videos_list': found_entries },
                          context_instance=RequestContext(request))
                            
@login_required(login_url='/login/')
def submit(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES or None)
            if form.is_valid():
                    cmodel = form.save()
                    if cmodel.originalFile:
                        if settings.USE_TRANLOADIT:
                            client = Client(settings.TRANSLOAD_AUTH_KEY, settings.TRANSLOAD_AUTH_SECRET)
                            params = None
                            if (cmodel.kind==0):
                                params = {
                                    'steps': {
                                        ':original': {
                                            'robot': '/http/import',
                                            'url': cmodel.originalFile.url,
                                        }
                                    },
                                    'template_id': settings.TRANSLOAD_TEMPLATE_VIDEO_ID,
                                    'notify_url': settings.TRANSLOAD_NOTIFY_URL
                                }
                            if (cmodel.kind==1):
                                params = {
                                    'steps': {
                                        ':original': {
                                            'robot': '/http/import',
                                            'url': cmodel.originalFile.url,
                                        }
                                    },
                                    'template_id': settings.TRANSLOAD_TEMPLATE_AUDIO_ID,
                                    'notify_url': settings.TRANSLOAD_NOTIFY_URL
                                }
                            if (cmodel.kind==2):
                                params = {
                                    'steps': {
                                        ':original': {
                                            'robot': '/http/import',
                                            'url': cmodel.originalFile.url,
                                        }
                                    },
                                    'template_id': settings.TRANSLOAD_TEMPLATE_VIDEO_AUDIO_ID,
                                    'notify_url': settings.TRANSLOAD_NOTIFY_URL
                                }
                            result = client.request(**params)
                            cmodel.assemblyid = result['assembly_id']
                            cmodel.published = True
                            cmodel.encodingDone = False
                            cmodel.save()
                        else:
                            cmodel.save()
                            djangotasks.register_task(cmodel.encode_media, "Encode the files using ffmpeg")
                            encoding_task = djangotasks.task_for_object(cmodel.encode_media)
                            djangotasks.run_task(encoding_task)
                    if settings.USE_BITTORRENT:
                        djangotasks.register_task(cmodel.create_bittorrent, "Create Bittorrent File for Video and serve it")
                        torrent_task = djangotasks.task_for_object(cmodel.create_bittorrent)
                        djangotasks.run_task(torrent_task)
                    return redirect(list)
    
            return render_to_response('videos/submit.html',
                                    {'submit_form': form},
                                    context_instance=RequestContext(request))
        else:
            form = VideoForm()
            return render_to_response('videos/submit.html',
                                    {'submit_form': form},
                                    context_instance=RequestContext(request))
    else:
        return render_to_response('videos/nothing.html',
                            context_instance=RequestContext(request))
@csrf_exempt
def encodingdone(request):
    if request.method == 'POST':
        data = json.loads(request.POST['transloadit'])
        try:
            video = Video.objects.get(assemblyid=data['assembly_id'])
            if (video.kind == 0):
                results = data['results']
                resultItem = results[settings.TRANSLOAD_MP4_ENCODE]
                resultFirst = resultItem[0]
                video.mp4URL = resultFirst['url']
                video.mp4Size = resultFirst['size']
                resultMeta = resultFirst['meta']
                video.duration = str(resultMeta['duration'])
                resultItem = results[settings.TRANSLOAD_WEBM_ENCODE]
                resultFirst = resultItem[0]
                video.webmURL = resultFirst['url']
                video.webmSize = resultFirst['size']
                resultItem = results[settings.TRANSLOAD_THUMB_ENCODE]
                resultFirst = resultItem[0]
                video.videoThumbURL = resultFirst['url']
                os.remove(video.originalFile.path)
                video.originalFile = ""
            elif (video.kind == 1):
                results = data['results']
                resultItem = results[settings.TRANSLOAD_MP3_ENCODE]
                resultFirst = resultItem[0]
                video.mp3URL = resultFirst['url']
                video.mp3Size = resultFirst['size']
                resultMeta = resultFirst['meta']
                video.duration = str(resultMeta['duration'])
                resultItem = results[settings.TRANSLOAD_OGG_ENCODE]
                resultFirst = resultItem[0]
                video.oggURL = resultFirst['url']
                video.oggSize = resultFirst['size']
                os.remove(video.originalFile.path)
                video.originalFile = ""
            elif (video.kind == 2):
                results = data['results']
                resultItem = results[settings.TRANSLOAD_MP4_ENCODE]
                resultFirst = resultItem[0]
                video.mp4URL = resultFirst['url']
                video.mp4Size = resultFirst['size']
                resultMeta = resultFirst['meta']
                video.duration = str(resultMeta['duration'])
                resultItem = results[settings.TRANSLOAD_WEBM_ENCODE]
                resultFirst = resultItem[0]
                video.webmURL = resultFirst['url']
                video.webmSize = resultFirst['size']
                resultItem = results[settings.TRANSLOAD_MP3_ENCODE]
                resultFirst = resultItem[0]
                video.mp3URL = resultFirst['url']
                video.mp3Size = resultFirst['size']
                resultItem = results[settings.TRANSLOAD_OGG_ENCODE]
                resultFirst = resultItem[0]
                video.oggURL = resultFirst['url']
                video.oggSize = resultFirst['size']
                resultItem = results[settings.TRANSLOAD_THUMB_ENCODE]
                resultFirst = resultItem[0]
                video.videoThumbURL = resultFirst['url']
                os.remove(video.originalFile.path)
                video.originalFile = ""
            video.encodingDone = True
            video.save()
        except Video.DoesNotExist:
            raise Http404
        return HttpResponse("Video was updated")

    else:
        return render_to_response('videos/nothing.html',
                            context_instance=RequestContext(request))
    

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query                      
