from django.db import models
from datetime import datetime, timedelta
    
class CreatorTheme(models.Model):
    type = models.CharField(max_length = 140)

    def __unicode__(self):
        return self.type + " theme"

class Creator(models.Model):
    name = models.CharField(max_length = 140)
    location = models.CharField(max_length = 140)
    remote_thumb = models.URLField(blank = True)
    local_thumb = models.ImageField(upload_to = "image/upload/%Y/%m/%d", blank = True)
    themes = models.ManyToManyField(CreatorTheme)
    synopsis = models.TextField();
    
    def tumbnail():
        if local_thumb:
            return local_thumb
        return remote_thumb
    
    def __unicode__(self):
        return self.name
    
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
    
class Video(models.Model):
    video = models.FileField(upload_to = "video/%Y/%m/%d", blank = True)
    title = models.CharField(max_length = 140)
    file_name = models.CharField(max_length = 400)
    
    def __unicode__(self):
        return self.title + " video"
    
class Event(models.Model):
    creator = models.ForeignKey(Creator)
    room = models.ForeignKey(Room)
    name = models.CharField(max_length = 140)
    description = models.TextField(blank = True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def validateEndDate():
        if(end < start):
            end = start + timedelta(minutes = 30)
    
    def __unicode__(self):
        return self.name + " with " + self.creator.name

class CreatorChip(models.Model):
    creator = models.ForeignKey(Creator)
    video = models.ForeignKey(Video)
    relatedChips = models.ManyToManyField('self', null = True, blank = True, symmetrical = False)
    
    def __unicode__(self):
        return self.creator.name + " / " + self.video.title + " chip "
        
class Status(models.Model):
    MOD_STATES = (  ("dead", "Not Used"),
                    ("major", "Major Status"),
                    ("minor", "Minor Status"),
                 )

    state = models.CharField(max_length = 5, choices = MOD_STATES, default = "dead")
    created = models.DateTimeField()
    status = models.CharField(max_length = 140)
    user = models.CharField(max_length = 140)
    room = models.ForeignKey(Room)
    
    def __unicode__(self):
        return self.status

class LivePhoto(models.Model):
    image = models.ImageField(upload_to = "image/photos/%H/%m")
    created = models.DateTimeField(auto_now_add = True)