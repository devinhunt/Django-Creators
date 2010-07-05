from django.contrib import admin
from creators.models import *

class RoomInline(admin.TabularInline):
    model = Room

class FloorAdmin(admin.ModelAdmin):
    inlines = [
        RoomInline,
    ]
    
class CreatorAdmin(admin.ModelAdmin):
    inlines = [
        
    ]

admin.site.register(Status)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(Room)
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Photo)
admin.site.register(PartyUser)