from creators.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings

# User GET Methods

def users(request):
    return api_response(True, "All users", serializers.serialize("json", PartyUser.objects.all(), ensure_ascii = True))

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
        
        return api_response(True, 'User created', serializers.serialize("json", [user], ensure_ascii = True))
    else:
        return api_response(False, 'No username specified.')
        
def user_list_friends(request):
    user = get_user_from_key(request)
    return api_response(True, 'List of friends for %s' % user.name, serializers.serialize('json', user.friends.all(), ensure_ascii = True))
    
def user_list_friend_status(request):
    user = get_user_from_key(request)
    statuses = []
    
    for friend in user.friends.all():
        if friend.current_status:
            statuses.append(friend.current_status)
    
    return api_response(True, 'List of friends for %s' % user.name, serializers.serialize('json', statuses, ensure_ascii = True))
    pass
        
# User POST methods

def user_add_friend(request):
    user = get_user_from_key(request)
    
    try:
        friend = PartyUser.objects.get(name = request.POST['username'])
        
        try:
            current_friend = user.friends.get(pk = friend.pk)
            return api_response(False, '%s has already friended %s' % (user.name, friend.name))
        except:
            user.friends.add(friend)
            return api_response(True, friend.name + " added as friend.", serializers.serialize("json", [user], ensure_ascii = True))
    except:
        return api_response(False, "The friend you wish to add does not exist.")
        
def user_remove_friend(request):
    user = get_user_from_key(request)
    
    try:
        friend = PartyUser.objects.get(name = request.POST['username'])
        user.friends.remove(friend)
        return api_response(True, "Friendship broken.")
    except:
        return api_response(False, "No friendship found.")
        
def user_checkin(request):
    user = get_user_from_key(request)
    user.x = request.POST.get('x')
    user.y = request.POST.get('y')
    user.current_floor = Floor.objects.get(pk = request.POST.get('floor'))
    user.save()
    return api_response(True, 'User checked in')
        
#Status GET

def status(request, pk = None):
    if pk:
        return HttpResponse(serializers.serialize("json", Status.objects.filter(pk__gt = pk).order_by('-created'), ensure_ascii = True))
    else:

        return HttpResponse(serializers.serialize("json", Status.objects.all().order_by('-created'), ensure_ascii = True))

#Status POST

def add_status(request):
    if request.method == 'POST':
        user = get_user_from_key(request)
        msg = request.POST.get('status')
        
        status = Status(status = msg, author = user.name)
        status.save()
        
        user.current_status = status;
        user.save()
        
        return api_response(True, 'Status set for %s' % (user.name), serializers.serialize("json", [status], ensure_ascii = True))
    else:
        return api_response(False, 'Bad POST data')

# Event GET
def events(request):
    return api_response(True, 'All Events', serializers.serialize("json", Event.objects.all(), ensure_ascii = True))

# Photo
def photo(request, pk = None):
    return api_response(True, 'All Photos', serializers.serialize("json", Photo.objects.all().order_by('-created'), ensure_ascii = True))

def photo_upload(request):
    if request.method == 'POST':
        print request.FILES
        photo = Photo(image = request.FILES['photo'])
        photo.save()
        return api_response(False, 'Upload Successful')
    else:
        return api_response(False, 'Improper POST data')

# Direct Model Access
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
    
def json_livephoto(request, pk = None):
    return HttpResponse(serializers.serialize("json", LivePhoto.objects.all().order_by('-created'), ensure_ascii = True))
    
def json_livephoto_latest(request):
    photo = LivePhoto.objects.all().order_by('-pk')[0:1]
    return HttpResponse(serializers.serialize("json", photo, ensure_ascii = True))
    
# Helper Function

def get_user_from_key(request):
    if request.method == 'POST':
        print request.POST['key']
        return get_object_or_404(PartyUser, api_key = request.POST['key']);
    else:
        return get_object_or_404(PartyUser, api_key = request.GET['key']);
    
def api_response(success, msg = '', data = None):
    response = '{"success" : "%s", "msg" : "%s"' % (success, msg)
    
    if data:
        response = response + ', "data" : %s' % data
    response = response + '}'
    
    return HttpResponse(response)


# Urls

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Users
    url(r'^user/$', users, name = "api_users"),
    url(r'^user/create/$', user_create, name = "api_user_create"),
    url(r'^user/checkin/$', user_checkin, name = "api_user_checkin"),
    url(r'^user/friends/$', user_list_friends, name = "api_list_friends"),
    url(r'^user/friends/add/$', user_add_friend, name = "api_add_friend"),
    url(r'^user/friends/remove/$', user_remove_friend, name = "api_remove_friend"),
    url(r'^user/friends/status/$', user_list_friend_status, name = "api_list_friends_status"),
    url(r'^user/events/$', user_create, name = "api_list_events"),
    
    #Status'
    url(r'^status/$', status, name = "api_status"),
    url(r'^status/since/(?P<pk>\d+)$', status, name = "api_status_since"),
    url(r'^status/add/$', add_status, name = "api_add_status"),
    
    #Events
    url(r'^events/$', events, name = "api_events"),
    
    #Rooms
    url(r'^room/$', json_room, name = "api_room"),
    url(r'^floor/$', json_floor, name = "api_floor"),
    
    #Photo
    url(r'^photo/$', photo, name = "api_photo"),
    url(r'^photo/upload/$', photo_upload, name = "api_photo_upload"),
    
    url(r'^creator/$', json_creator, name = "api_creator"),
    url(r'^creatorchips/$', json_creator_chips, name = "api_creator_chips"),
    url(r'^videos/$', json_videos, name = "api_videos"),
    
    url(r'^livephoto/$', json_livephoto, name = "api_livephoto"),
    url(r'^livephoto/latest/', json_livephoto_latest, name = "api_livephoto_latest"),
)