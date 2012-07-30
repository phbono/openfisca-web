from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'simulation.views.index'),
    url(r'^menage/$', 'simulation.views.menage'),
    url(r'^logement/$', 'simulation.views.logement'),
    url(r'^output/$', 'simulation.views.output'),
    url(r'^graph.png$', 'simulation.views.graph', name='graph'),
    url(r'^home/$', 'simulation.views.home', name='home'),
)