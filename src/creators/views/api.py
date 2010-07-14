from creators.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import datetime;

hack_day_date = datetime(2010, 7, 18)

# User GET Methods
def users(request):
    return api_response(True, "All users", serializers.serialize("json", PartyUser.objects.all(), ensure_ascii = True))

def user_create(request):
    request_name = request.GET.get('username', 'Guest').upper()
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
        
def user_exists(request):
    try:
        user = PartyUser.objects.get(api_key = request.GET['key'])
        return api_response(True, 'User exists', serializers.serialize("json", [user], ensure_ascii = True))
    except:
        return api_response(False, 'No user by that key.')
        
def user_list_friends(request):
    user = get_user_from_key(request)
    return api_response(True, 'List of friends for %s' % user.name, serializers.serialize('json', user.friends.all(), ensure_ascii = True))
    
def user_list_friend_status(request):
    user = get_user_from_key(request)
    statuses = []
    
    for friend in user.friends.all():
        if friend.current_status:
            statuses.append(friend.current_status)
    
    return api_response(True, 'List of friend statuses for %s' % user.name, serializers.serialize('json', statuses, ensure_ascii = True))
    pass
    
def user_events(request):
    user = get_user_from_key(request)
    return api_response(True, 'All user favorite events', serializers.serialize('json', user.events.all(), ensure_ascii = True))
    
    
# User POST methods

def user_rename(request):
    user = get_user_from_key(request)
    user.name = request.POST.get('username').upper()
    user.save()
    return api_response(True, 'User name changed', serializers.serialize("json", [user], ensure_ascii = True))
    
def user_add_friend(request):
    user = get_user_from_key(request)
    
    try:
        friend = PartyUser.objects.get(name = request.POST['username'].upper())
        
        try:
            current_friend = user.friends.get(pk = friend.pk)
            return api_response(False, '%s has already friended %s' % (user.name, friend.name), serializers.serialize("json", [user], ensure_ascii = True))
        except:
            user.friends.add(friend)
            return api_response(True, friend.name + " added as friend.", serializers.serialize("json", [user], ensure_ascii = True))
    except:
        return api_response(False, "The friend you wish to add does not exist.")
        
def user_remove_friend(request):
    user = get_user_from_key(request)
    
    try:
        friend = PartyUser.objects.get(name = request.POST['username'].upper())
        user.friends.remove(friend)
        return api_response(True, "Friendship broken.", serializers.serialize('json', [user], ensure_ascii = True))
    except:
        return api_response(False, "No friendship found.")
        
def user_checkin(request):
    user = get_user_from_key(request)
    
    user.x = int(request.POST.get('x'))
    user.y = int(request.POST.get('y'))
    user.current_floor = Floor.objects.get(pk = request.POST.get('floor'))
    
    if user.set_current_room():
        user.checkin_time = datetime.now()
        user.save()
        return api_response(True, 'User checked in')
        
    return api_response(False, 'No Valid Room Found')

def user_add_event(request):
    user = get_user_from_key(request)
    try:
        event = Event.objects.get(pk = request.POST.get('eid'))
        user.events.add(event)
        return api_response(True, "Event added to user", serializers.serialize('json', [user], ensure_ascii = True))
    except:
        return api_response(False, "No matching event")
    

def user_remove_event(request):
    user = get_user_from_key(request)
    try:
        event = Event.objects.get(pk = request.POST.get('eid'))
        user.events.remove(event)
        return api_response(True, "Event Removed", serializers.serialize('json', [user], ensure_ascii = True))
    except:
        return api_response(False, "No matching event")
        

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
    result = '{ "events" : %s, "event_types": %s}' % (serializers.serialize("json", Event.objects.all(), ensure_ascii = True),
                                                      serializers.serialize("json", EventType.objects.all(), ensure_ascii = True))
    return api_response(True, 'All Events', result)
    
def events_hack(request):
    events = Event.objects.all()
    result = '{ "events" : %s, "event_types": %s}' % (bad_date_json(events),
                                                      serializers.serialize("json", EventType.objects.all(), ensure_ascii = True))
    return api_response(True, 'All Events', result)

def bad_date_json(events):
    result = '['
    first_loop = True
    
    for event in events:
        if first_loop:
            first_loop = False
        else:
            result += ', '
            
        if event.start >= hack_day_date:
            start_str = '%s _%s:%s' % (event.start.strftime('%Y-%m-%d '), event.start.hour, event.start.strftime('%M:%S'))
        else:
            start_str = event.start.strftime('%Y-%m-%d %H:%M:%S')
        
        if event.end >= hack_day_date:
            end_str = '%s _%s:%s' % (event.end.strftime('%Y-%m-%d '), event.end.hour, event.end.strftime('%M:%S'))
        else:
            end_str = event.end.strftime('%Y-%m-%d %H:%M:%S')
            
        result += '{"pk": %s, "model": "creators.event", "fields": {"detail_url": "%s", "end": "%s", "event_type": %s, "creator": %s, "name": "%s", "start": "%s", "room": %s, "icon": %s, "description": "%s"}}' % (event.pk, 
            event.detail_url, end_str, hack_get_pk(event.event_type), hack_get_pk(event.creator), event.name, start_str, hack_get_pk(event.room), hack_get_pk(event.icon, True), event.description)

    result += ']'
    return result
    
def hack_get_pk(obj, quoted = False):
    try:
        if quoted:
            return '"%s"' % (obj.pk)
        else:
            return obj.pk
    except:
        return 'null'

# Photo

def photo(request, pk = None):
    return api_response(True, 'All Photos', serializers.serialize("json", Photo.objects.filter(state="live").order_by('-created')[:50], ensure_ascii = True))

def photo_upload(request):
    if request.method == 'POST':
        photo = Photo(image = request.FILES['photo'], author = request.POST.get('author', ''))
        photo.save()
        return api_response(True, 'Upload Successful')
    else:
        return api_response(False, 'Improper POST data')


# Assets

def assets(request):
    asset_key = request.GET.get("key", None)
    if asset_key:
        return api_response(True, "Single Asset", serializers.serialize("json", [Asset.objects.get(key = asset_key)], ensure_ascii = True))
    else:
        return api_response(True, "Full Asset List", serializers.serialize("json", Asset.objects.all(), ensure_ascii = True))


# Direct Model Access

def json_creator(request):
    return api_response(True, 'All Creators', serializers.serialize("json", Creator.objects.all(), ensure_ascii = True))
    
def json_videos(request):
    return HttpResponse(serializers.serialize("json", Video.objects.all(), ensure_ascii = True))

def json_room(request):
    return api_response(True, 'All Rooms', serializers.serialize("json", Room.objects.all(), ensure_ascii = True))

def json_floor(request):
    return api_response(True, 'All Floors', serializers.serialize("json", Floor.objects.all(), ensure_ascii = True))


# Helper Function

def get_user_from_key(request):
    if request.method == 'POST':
        return get_object_or_404(PartyUser, api_key = request.POST['key']);
    else:
        return get_object_or_404(PartyUser, api_key = request.GET['key']);
    
def api_response(success, msg = '', data = None):
    valid_date = Metadata.objects.get(name = 'last_updated')
    
    response = '{"success" : "%s", "msg" : "%s", "last_updated" : "%s"' % (success, msg, valid_date.timestamp.__str__())
    
    if data:
        response = response + ', "data" : %s' % data
    response = response + '}'
    
    return HttpResponse(response)


# Urls

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Users
    url(r'^users/$', users, name = "api_users"),
    url(r'^users/exists/$', user_exists),
    url(r'^users/create/$', user_create, name = "api_user_create"),
    url(r'^users/rename/$', user_rename),
    url(r'^users/checkin/$', user_checkin, name = "api_user_checkin"),
    url(r'^users/friends/$', user_list_friends, name = "api_list_friends"),
    url(r'^users/friends/add/$', user_add_friend, name = "api_add_friend"),
    url(r'^users/friends/remove/$', user_remove_friend, name = "api_remove_friend"),
    url(r'^users/friends/status/$', user_list_friend_status, name = "api_list_friends_status"),
    url(r'^users/events/$', user_events),
    url(r'^users/events/add/$', user_add_event),
    url(r'^users/events/remove/$', user_remove_event),
    
    
    # Status'
    url(r'^status/$', status, name = "api_status"),
    url(r'^status/since/(?P<pk>\d+)$', status, name = "api_status_since"),
    url(r'^status/add/$', add_status, name = "api_add_status"),
    
    # Events
    url(r'^events/$', events_hack),
    url(r'^events/normal/$', events),
    
    # Rooms
    url(r'^rooms/$', json_room, name = "api_room"),
    url(r'^floors/$', json_floor, name = "api_floor"),
    
    # Photo
    url(r'^photos/$', photo, name = "api_photo"),
    url(r'^photos/upload/$', photo_upload, name = "api_photo_upload"),
    
    # Raw Image Assets
    url(r'^assets/$', assets),
    
    # Direct Model Access
    url(r'^creators/$', json_creator, name = "api_creator"),
    url(r'^videos/$', json_videos, name = "api_videos"),
)