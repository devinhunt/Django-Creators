from django.contrib import admin
from creators.models import *

class RoomInline(admin.TabularInline):
    model = Room

class FloorAdmin(admin.ModelAdmin):
    inlines = [
        RoomInline,
    ]
    
class CreatorThemeInline(admin.TabularInline):
    model = CreatorTheme
    
class CreatorAdmin(admin.ModelAdmin):
    inlines = [
        #CreatorThemeInline,
    ]

admin.site.register(Alert);
admin.site.register(Creator, CreatorAdmin);
admin.site.register(CreatorTheme);
admin.site.register(Floor, FloorAdmin);
admin.site.register(Room);
admin.site.register(Video);
admin.site.register(Event);
admin.site.register(CreatorChip);