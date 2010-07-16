from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from creators.models import *


def index(request):
    return render_to_response('index.html', {})
    
def news(request):
    minor_statuses = Status.objects.exclude(state = 'dead').order_by('-created')[:40]
    return render_to_response('news.html', {'statuses' : minor_statuses} )

# Urls

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Default and Landing
    url(r'^$', index),
)