import sys, urllib, json
from creators.models import *
from datetime import datetime, timedelta

creators_url = "http://www.thecreatorsproject.com/api/creators.json"
interface_api = "http://at.thecreatorsproject.com/party/interface.php"
valid_event_types = ["music", "art", "film", "panel"]

def scrape():
    scrapeRooms();
    scrapeEvents();

def scrapeCreators():
    print "INFO :: Starting a scrape of creators."
    
    creators_ref = urllib.urlopen(creators_url)
    creators_obj = json.load(creators_ref)
    
    for creator_obj in creators_obj:
        try:
            creator = Creator.objects.get(name = creator_obj["name"])
        except:
            creator = Creator(name = creator_obj["name"], location = creator_obj["location"], remote_thumb = creator_obj["small-chip"])
            creator.save();
        
            for theme_str in creator_obj["themes"]:
                try:
                    theme = CreatorTheme.objects.get(type = theme_str)
                except:
                    theme = CreatorTheme(type = theme_str)
                    theme.save()
            
                creator.themes.add(theme)
            print "Added %s" % creator.__unicode__();
            
def scrapeRooms():
    print 'INFO :: Starting a scrape of rooms.'
    
    room_objs = json.load(urllib.urlopen(interface_api + '?type=list_all_rooms'))
    
    for room_obj in room_objs:
        floor, created = Floor.objects.get_or_create(order = room_obj['floor'])
        room, created = Room.objects.get_or_create( pk = room_obj['id'],
                                                    name = room_obj['name'], 
                                                    floor = floor,
                                                    x = room_obj['x'],
                                                    y = room_obj['y'],
                                                    width = room_obj['width'],
                                                    height = room_obj['height'])

def scrapeEvents():
    print 'INFO :: Starting a scrape of events.'
    event_objs = json.load(urllib.urlopen(interface_api + '?type=list_events'))
    default_creator, created = Creator.objects.get_or_create(name = "Default Creator", location = "Your Attic", synopsis = "He doesn't really exist.")
    
    for event_obj in event_objs:
        start_time = datetime.now()
        end_time = datetime.now()
        description = event_obj['description']
        if description == None:
            description = ""
        
        event_floor = event_obj['floor']
        if(event_floor == '8'):
            event_floor = '3';
        
        floor, created = Floor.objects.get_or_create(order = event_floor)
        room, created = Room.objects.get_or_create(name = event_obj['room_name'], floor = floor)
        event, created = Event.objects.get_or_create( name = event_obj['name'],
                                                      creator = default_creator,
                                                      room = room,
                                                      description = description,
                                                      start = start_time,
                                                      end = end_time)

def main(*args):
    try:
        scrape()
    except:
        print "There was an error scrapping."
        pass
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv))