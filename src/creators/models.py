from django.db import models
from datetime import datetime, timedelta
import hashlib

class Floor(models.Model):
    order = models.IntegerField(default = 0)
    name = models.CharField(max_length = 140, blank = True)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length = 140)
    floor = models.ForeignKey(Floor)
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    width = models.IntegerField(default = 100)
    height = models.IntegerField(default = 100)

    def __unicode__(self):
        return self.name + " on the " + self.floor.name

class Creator(models.Model):
    CREATOR_THEMES = (("music", "Musician"),
                      ("film", "Film"),
                      ("fashion", "Fashion"),
                     )
    name = models.CharField(max_length = 200)
    theme = models.CharField(max_length = 10, choices = CREATOR_THEMES)
    local_thumbname = models.CharField(max_length = 200, blank = True)
    thumbnail = models.ImageField(upload_to = "image/upload/chips/%Y-%m-%d", blank = True)
    description = models.TextField(blank = True)
    
    
    def __unicode__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length = 140)
    is_static = models.BooleanField(default = False)
        
class Event(models.Model):
    name = models.CharField(max_length = 140)
    creator = models.ForeignKey(Creator)
    room = models.ForeignKey(Room)
    event_type = models.ForeignKey(EventType)
    description = models.TextField(blank = True)
    detail_url = models.URLField(blank = True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def forceValidEnd():
        if(end < start):
            end = start + timedelta(minutes = 15)

    def __unicode__(self):
        return self.name + " with " + self.creator.name
    
class Status(models.Model):
    MOD_STATES = (  ("dead", "Not Used"),
                    ("major", "Major Status"),
                    ("minor", "Minor Status"),
                 )

    state = models.CharField(max_length = 5, choices = MOD_STATES, default = "dead")
    created = models.DateTimeField(default = datetime.now())
    status = models.CharField(max_length = 140)
    author = models.CharField(max_length = 140) 

    def __unicode__(self):
        return '[' + self.state + '] ' + self.status
        
class PartyUser(models.Model):
    name = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add = True)
    api_key = models.CharField(max_length = 100, blank = True)
    phone_number = models.CharField(max_length = 20, blank = True)
    
    x = models.IntegerField(default = 0)
    y = models.IntegerField(default = 0)
    
    current_status = models.ForeignKey(Status, blank = True, null = True)
    current_room = models.ForeignKey(Room, blank = True, null = True)
    friends = models.ManyToManyField('self', blank = True, null = True, symmetrical = False)
    events = models.ForeignKey(Event, blank = True, null = True)
    
    def save(self, *args, **kwargs):
        '''Overrideen save function generates the api key for the user'''
        if not self.api_key:
            self.api_key = hashlib.md5(datetime.now().isoformat() + " " + self.name).hexdigest()
        super(PartyUser, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name + ' (created ' + self.created.isoformat() + ')'

class Photo(models.Model):
    image = models.ImageField(upload_to = "image/upload/photo/%Y-%m-%d")
    created = models.DateTimeField(auto_now_add = True)
    author = models.CharField(max_length = 140, blank = True)