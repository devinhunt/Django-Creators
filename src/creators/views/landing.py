from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html', {})
    
def news(request):
    return render_to_response('news.html', {})

# Urls

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Default and Landing
    url(r'^$', index),
)