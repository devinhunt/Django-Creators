import sys, urllib, json
from creators.models import *

creators_url = "http://www.thecreatorsproject.com/api/creators.json"

def scrape():
    scrapeCreators()
    scrapeEvents()

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
    pass
    
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