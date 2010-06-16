from django.contrib import admin
from creators.models import *

class RoomInline(admin.TabularInline):
    model = Room

class FloorAdmin(admin.ModelAdmin):
    inlines = [
        RoomInline,
    ]

admin.site.register(Alert);
admin.site.register(Creator);
admin.site.register(Floor, FloorAdmin);
admin.site.register(Room);
admin.site.register(Video);
admin.site.register(EventChip);
admin.site.register(CreatorChip);