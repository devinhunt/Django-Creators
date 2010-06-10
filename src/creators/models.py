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
    
class Place(models.Model):
    name = models.CharField(max_length = 140)
    
    def __unicode__(self):
        return self.name
    
class Video(models.Model):
    creator = models.ForeignKey(Creator)
    video = models.FileField(upload_to = "video/%Y/%m/%d")
    title = models.CharField(max_length = 140)
    
    def __unicode__(self):
        return self.title + " for " + self.creator.name
    
class EventChip(models.Model):
    creator = models.ForeignKey(Creator)
    name = models.CharField(max_length = 140)
    description = models.TextField()
    place = models.ForeignKey(Place)
    start = models.DateTimeField(auto_now_add = True)
    end = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.name + " with " + self.creator.name

class CreatorChip(models.Model):
    creator = models.ForeignKey(Creator)
    video = models.ForeignKey(Video, blank = True)
    realtedChips = models.ForeignKey('self', blank = True)
    
    def __unicode__(self):
        return self.creator.name + "chip"