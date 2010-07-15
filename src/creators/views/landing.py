from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from creators.models import *


def index(request):
    return render_to_response('index.html', {})
    
def news(request):
    minor_statuses = Status.objects.filter(state = 'minor').order_by('-created')[:40]
    try:
        major_status = Status.objects.filter(state = 'major').order_by('-created')[0]
    except:
        major_status = None
    return render_to_response('news.html', {'statuses' : minor_statuses, 'major_status' : major_status})

# Urls

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Default and Landing
    url(r'^$', index),
)