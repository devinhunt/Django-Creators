from creators.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

# Direct Model Access

def json_schedule(request):
    return HttpResponse(serializers.serialize("json", Event.objects.all(), ensure_ascii = True))
    
def json_creator(request, id = None):
    return HttpResponse(serializers.serialize("json", Creator.objects.all(), ensure_ascii = True))

def json_room(request, id = None):
    return HttpResponse(serializers.serialize("json", Room.objects.all(), ensure_ascii = True))

def json_floor(request, id = None):
    if id:
        pass
    return HttpResponse(serializers.serialize("json", Floor.objects.all(), ensure_ascii = True))

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^schedule/$', json_schedule, name = "json_schedule"),
    url(r'^creator/$', json_creator, name = "json_creator"),
    url(r'^room/$', json_room, name = "json_room"),
    url(r'^floor/$', json_floor, name = "json_floor"),
)