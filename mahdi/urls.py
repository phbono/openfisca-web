from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'mahdi.views.index'),
    url(r'^menage/$', 'mahdi.views.menage'),
)