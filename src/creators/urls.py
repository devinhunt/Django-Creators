from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #Default landing
    (r'^$', include('creators.views.landing')),
    (r'^news/', 'creators.views.landing.news'),
    
    # services
    (r'^api/', include('creators.views.api')),
    
    # administration 
    (r'^admin/', include(admin.site.urls)),
    
    #media
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/www/hailpixel/django-creators/media/'}),
)