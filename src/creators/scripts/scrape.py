import sys, urllib, json
from creators.models import *

vice_url = "http://www.thecreatorsproject.com/api/creators.json"

def scrape():
    print "Starting a scrape of %s" % vice_url
    creators_ref = urllib.urlopen(vice_url)
    creators_obj = json.load(creators_ref)
    
    for creator_obj in creators_obj:
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
    
def main(*args):
    #try:
    scrape()
    #except:
    #    print "There was an error"
    #    pass
    #else:
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv))