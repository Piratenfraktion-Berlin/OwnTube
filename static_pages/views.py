from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

# All this views are just showing static pages not really usefull

def contact(request):
    return render_to_response('static_pages/contact.html',context_instance=RequestContext(request))
    
def about(request):
    return render_to_response('static_pages/about.html',context_instance=RequestContext(request))