from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'index'),
    
    # services
    (r'^api/', include('creators.views.api')),
    
    # administration 
    (r'^admin/', include(admin.site.urls))
)