from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'simulation.views.index'),
    url(r'^menage/$', 'simulation.views.menage'),
)