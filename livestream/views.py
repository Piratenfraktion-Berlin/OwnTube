from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from livestream.models import Stream

import datetime


def current(request):
    ''' This view gets all streams that are scheduled to be live right now
    if there are no streams it redirects to the liste view. The upcoming_streams_list
    is used to show upcoming events in a side bar (see the template)'''
	stream_list = Stream.objects.filter(published=True,startDate__lt=datetime.datetime.now, endDate__gt=datetime.datetime.now).order_by('-startDate')
	upcoming_streams_list = Stream.objects.filter(published=True,endDate__gt=datetime.datetime.now).order_by('-startDate')[:5]
	if not stream_list:
		return redirect(list)
	else:
		return render_to_response('livestream/current.html', {'stream_list': stream_list, 'upcoming_streams_list': upcoming_streams_list},
                            context_instance=RequestContext(request))


def list(request):
    ''' This view shows gets all upcoming streaming events
    and forwards them to our template '''
    stream_list = Stream.objects.filter(published=True,endDate__gt=datetime.datetime.now).order_by('-startDate')
    return render_to_response('livestream/list.html', {'stream_list': stream_list},
                            context_instance=RequestContext(request))

def detail(request, slug):
    ''' This view shows the detail of a stream, it is used to
    show the user more information on one event but not
    for showing the player'''
    stream = get_object_or_404(Stream, slug=slug)
    upcoming_streams_list = Stream.objects.filter(published=True,endDate__gt=datetime.datetime.now).order_by('-startDate')[:5]
    return render_to_response('livestream/detail.html', {'stream': stream, 'upcoming_streams_list': upcoming_streams_list},
                            context_instance=RequestContext(request))