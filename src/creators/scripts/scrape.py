import sys, urllib, json
from creators.models import *
from datetime import datetime, timedelta

creators_url = "http://www.thecreatorsproject.com/api/creators.json"
events_url = "http://ec2-204-236-200-105.compute-1.amazonaws.com/party/interface.php?type=list_raw_events"
valid_event_types = ["music", "art", "film", "panel"]

def scrape():
    scrapeCreators()
    scrapeEvents()

def scrapeCreatorsLocal():
    ''' This is some hardcore hacks'''
    

def scrapeCreators():
    print "Starting a scrape of %s" % creators_url
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
        
def scrapeEvents():
    print "Starting a scrape of all events on %s" % events_url
    bad_date = "0000-00-00 00:00:00"
    event_objs = json.load(urllib.urlopen(events_url))
    
    default_creator, created = Creator.objects.get_or_create(name = "Default Creator", location = "New York")
    if created:
        default_creator.save()
    
    for event_obj in event_objs:
        if event_obj["type"] in valid_event_types:
            ev_floor, created = Floor.objects.get_or_create(order = event_obj["floor"]);
            ev_floor.save()
        
            ev_room, created = Room.objects.get_or_create(name = event_obj["room_name"], floor = ev_floor)
            ev_room.save()
            
            
            if event_obj["description"] == None:
                ev_description = "none"
            else:
                ev_description = event_obj["description"]
            
            
            start_date = datetime.strptime(event_obj["time_start"], "%Y-%m-%d %H:%M:%S")
            try:
                end_date = datetime.strptime(event_obj["time_end"], "%Y-%m-%d %H:%M:%S")
            except:
                end_date = start_date + timedelta(hours = 1)
        
            new_event, created = Event.objects.get_or_create(name = event_obj["name"], 
                                                room = ev_room, 
                                                start = start_date, 
                                                end = end_date, 
                                                description = ev_description,
                                                creator = default_creator)
            new_event.save()
    
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