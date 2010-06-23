from django.db import models

class Alert(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 140)
    message = models.TextField()
    
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
    
    def __unicode__(self):
        return self.name + " on the " + self.floor.name
    
class Video(models.Model):
    creator = models.ForeignKey(Creator)
    video = models.FileField(upload_to = "video/%Y/%m/%d")
    title = models.CharField(max_length = 140)
    hash = models.CharField(max_length = 400)
    
    def __unicode__(self):
        return self.title + " for " + self.creator.name
    
class Event(models.Model):
    creator = models.ForeignKey(Creator, blank = True)
    room = models.ForeignKey(Room)
    name = models.CharField(max_length = 140)
    description = models.TextField(blank = True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __unicode__(self):
        return self.name + " with " + self.creator.name

class CreatorChip(models.Model):
    creator = models.ForeignKey(Creator)
    video = models.ForeignKey(Video, blank = True)
    realtedChips = models.ForeignKey('self', blank = True)
    
    def __unicode__(self):
        return self.creator.name + " chip"