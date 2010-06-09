from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'index'),
    url(r'^dashboard/$', 'dashboard', name = "dashboard"),
    url(r'^dashboard/alert/add$', 'alert_add', name = "alert_add"),
    url(r'^dashboard/node/upload$', 'node_upload', name = "node_upload"),
    (r'^admin/', include(admin.site.urls))
)