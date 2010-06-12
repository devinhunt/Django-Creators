from django.db import models

class Alert(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 140)
    message = models.TextField()
    
class Creator(models.Model):
    CREATOR_TYPES = (
        ("musician", "Musician"),
        ("artist", "Artist"),
        ("fashion", "Fashion"),
    )
    
    name = models.CharField(max_length = 140)
    kind = models.CharField(max_length = 140, choices = CREATOR_TYPES)
    thumbnail = models.ImageField(upload_to = "image/upload/%Y/%m/%d")
    
    def __unicode__(self):
        return self.name + " (" + self.kind + ")";
    
class Floor(models.Model):
    order = models.IntegerField(default = 0)
    name = models.CharField(max_length = 140)
    
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
    
    def __unicode__(self):
        return self.title + " for " + self.creator.name
    
class EventChip(models.Model):
    creator = models.ForeignKey(Creator)
    room = models.ForeignKey(Room)
    name = models.CharField(max_length = 140)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __unicode__(self):
        return self.name + " with " + self.creator.name

class CreatorChip(models.Model):
    creator = models.ForeignKey(Creator)
    video = models.ForeignKey(Video, blank = True)
    realtedChips = models.ForeignKey('self', blank = True)
    
    def __unicode__(self):
        return self.creator.name + "chip"