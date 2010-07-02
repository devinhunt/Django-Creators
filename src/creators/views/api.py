from creators.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404

# User Methods

def user_create(request):
    request_name = request.GET.get('username', None)
    print request_name
    if request_name:
        count = 1
        user, created = PartyUser.objects.get_or_create(name = request_name)
        
        while not created:
            new_name = '%s%i' % (request_name, count)
            user, created = PartyUser.objects.get_or_create(name = new_name)
            count = count + 1
        
        return HttpResponse(serializers.serialize("json", [user], ensure_ascii = True))
        
    else:
        raise Http404

# Direct Model Access
def json_schedule(request):
    return HttpResponse('{ "events" : ' + serializers.serialize("json", Event.objects.all(), ensure_ascii = True) + ', ' +
                           '"chips" : ' + serializers.serialize("json", EventChip.objects.all(), ensure_ascii = True) + '}')
    
def json_creator(request):
    return HttpResponse(serializers.serialize("json", Creator.objects.all(), ensure_ascii = True))
    
def json_creator_chips(request):
    return HttpResponse(serializers.serialize("json", CreatorChip.objects.all(), ensure_ascii = True))
    
def json_videos(request):
    return HttpResponse(serializers.serialize("json", Video.objects.all(), ensure_ascii = True))

def json_room(request):
    return HttpResponse(serializers.serialize("json", Room.objects.all(), ensure_ascii = True))

def json_floor(request):
    return HttpResponse(serializers.serialize("json", Floor.objects.all(), ensure_ascii = True))
    
def json_status(request, pk = None):
    if pk:
        return HttpResponse(serializers.serialize("json", Status.objects.filter(pk__gt = pk), ensure_ascii = True))
    else:
        return HttpResponse(serializers.serialize("json", Status.objects.all(), ensure_ascii = True))
    
def json_livephoto(request, pk = None):
    return HttpResponse(serializers.serialize("json", LivePhoto.objects.all().order_by('-created'), ensure_ascii = True))
    
def json_livephoto_latest(request):
    photo = LivePhoto.objects.all().order_by('-pk')[0:1]
    return HttpResponse(serializers.serialize("json", photo, ensure_ascii = True))

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^user/create/$', user_create, name = "user_create"),
    url(r'^schedule/$', json_schedule, name = "json_schedule"),
    url(r'^creator/$', json_creator, name = "json_creator"),
    url(r'^creatorchips/$', json_creator_chips, name = "json_creator_chips"),
    url(r'^room/$', json_room, name = "json_room"),
    url(r'^floor/$', json_floor, name = "json_floor"),
    url(r'^videos/$', json_videos, name = "json_videos"),
    url(r'^status/$', json_status, name = "json_status"),
    url(r'^status/since/(?P<pk>\d+)$', json_status, name = "json_status_since"),
    url(r'^livephoto/$', json_livephoto, name = "json_livephoto"),
    url(r'^livephoto/latest/', json_livephoto_latest, name = "json_livephoto_latest"),
)