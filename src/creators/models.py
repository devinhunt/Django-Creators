from django.db import models
from datetime import datetime, timedelta
import hashlib

class Metadata(models.Model):
    name = models.CharField(max_length = 140)
    value = models.CharField(max_length = 140, blank = True)
    timestamp = models.DateTimeField()
    
    def __unicode__(self):
        return 'key %s ' % (self.name)
        
class Asset(models.Model):
    key = models.CharField(max_length = 100, primary_key = True)
    image = models.ImageField(upload_to = "image/asset/%Y-%m-%d")
    
    def __unicode__(self):
        return self.key
    
class IconBase(models.Model):
    ''' All models that need to use assets directly should extend this base '''
    icon = models.ForeignKey(Asset, null = True, blank = True)
    
    class Meta:
        abstract = True

class Floor(IconBase):
    order = models.IntegerField(default = 0)
    name = models.CharField(max_length = 140, blank = True)
    touchscreen_floor = models.BooleanField(default = False)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

class Room(IconBase):
    ROOM_TYPE = ( ("normal", "Normal Room"),
                  ("bathroom", "Bathroom"),
                  ("exit", "Exit"),
                  ("stairs", "Stairway"),
                  ("food", "Food"),
                  ("drinks", "Drinks"),
                  ("info", "Information Point"),
                  ("elevator", "Elevator"),
                )
    
    name = models.CharField(max_length = 140)
    room_type = models.CharField(max_length = 8, choices = ROOM_TYPE, default = "normal")
    
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    width = models.IntegerField(default = 10)
    height = models.IntegerField(default = 10)
    floor = models.ForeignKey(Floor)
    
    def contains_point(self, x, y):
        return x >= self.x and x <= (self.x + self.width) and y >= self.y and y <= (self.y + self.height)
    
    def __unicode__(self):
        return self.name + " on the " + self.floor.name

class Creator(IconBase):
    CREATOR_THEMES = (("music", "Musician"),
                      ("film", "Film"),
                      ("fashion", "Fashion"),
                      ("artist", "Artist"),
                      ("photographer", "Photographer"),
                      ("dj", "DJ"),
                     )
    
    name = models.CharField(max_length = 200)
    theme = models.CharField(max_length = 20, choices = CREATOR_THEMES)
    description = models.TextField(blank = True)
    video_key = models.CharField(max_length = 40, blank = True, default = '')
    
    def __unicode__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length = 140)
    is_static = models.BooleanField(default = False)
    
    def __unicode__(self):
        return self.name + " type"

class Event(IconBase):
    name = models.CharField(max_length = 140)
    
    creator = models.ForeignKey(Creator)
    room = models.ForeignKey(Room)
    event_type = models.ForeignKey(EventType)
    description = models.TextField(blank = True)
    detail_url = models.URLField(blank = True)
    all_day = models.BooleanField(default = False)
    
    start = models.DateTimeField()
    end = models.DateTimeField()

    def forceValidEnd():
        if(end < start):
            end = start + timedelta(minutes = 15)

    def __unicode__(self):
        return self.name + " with " + self.creator.name
    
class StatusManager(models.Manager):
    def get_by_natural_key(self, status, author):
        return self.get(status = status, author = author)

class Status(models.Model):
    objects = StatusManager()
    
    MOD_STATES = (  ("dead", "Not Used"),
                    ("major", "Major Status"),
                    ("minor", "Minor Status"),
                 )

    state = models.CharField(max_length = 5, choices = MOD_STATES, default = "dead")
    created = models.DateTimeField(default = datetime.now())
    status = models.CharField(max_length = 140)
    author = models.CharField(max_length = 140)
    
    class Meta:
        unique_together = (('status', 'author'),)
            
    def natural_keys(self):
        return (self.status, self.author)

    def __unicode__(self):
        return '[' + self.state + '] ' + self.status
        
class PartyUser(models.Model):
    name = models.CharField(max_length = 100)
    api_key = models.CharField(max_length = 100, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    checkin_time = models.DateTimeField(blank = True, null = True)
    
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    
    friends = models.ManyToManyField('self', blank = True, null = True, symmetrical = False)
    events = models.ManyToManyField(Event, blank = True, null = True)
    
    current_status = models.ForeignKey(Status, blank = True, null = True)
    current_floor = models.ForeignKey(Floor, blank = True, null = True)
    current_room = models.ForeignKey(Room, blank = True, null = True)
    
    def save(self, *args, **kwargs):
        ''' Overriden save function generates the api key for the user '''
        if not self.api_key:
            self.api_key = hashlib.md5(datetime.now().isoformat() + " " + self.name).hexdigest()
        super(PartyUser, self).save(*args, **kwargs)
        
    def set_current_room(self):
        ''' Finds a match for current room, or sets the current room to null '''
        for room in self.current_floor.room_set.all():
            if room.contains_point(x = self.x, y = self.y):
                self.current_room = room
                return True
        return False
    
    def __unicode__(self):
        return self.name + ' (created ' + self.created.isoformat() + ')'

class Photo(models.Model):
    
    MOD_STATES = (  ("dead", "Not Used"),
                    ("live", "Live Photo"),
                 )
    
    image = models.ImageField(upload_to = "image/photo/%Y-%m-%d")
    state = models.CharField(max_length = 4, choices = MOD_STATES, default = "dead")
    created = models.DateTimeField(auto_now_add = True)
    author = models.CharField(max_length = 140, blank = True)
    
    def __unicode__(self):
        return "[%s] %s uploaded %s by %s" % (self.state, self.image, self.created.strftime("%a %H:%M"), self.author)