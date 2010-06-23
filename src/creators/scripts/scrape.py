import sys, urllib, json
from creators.models import *
from datetime import datetime, timedelta

creators_url = "http://www.thecreatorsproject.com/api/creators.json"
events_url = "http://ec2-204-236-200-105.compute-1.amazonaws.com/party/interface.php?type=list_raw_events"
interface_api = "http://at.thecreatorsproject.com/party/interface.php"
valid_event_types = ["music", "art", "film", "panel"]

def scrape():
    scrapeCreators()
    scrapeEvents()

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
    print "INFO :: Starting a scrape of rooms."
    
    
    
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