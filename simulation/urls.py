from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^home/$', 'simulation.views.home', name='home'),
    url(r'^menage/$', 'simulation.views.menage'),
    url(r'^logement/$', 'simulation.views.logement'),
    url(r'^declar01/(?P<idfoy>\d{1})/$', 'simulation.views.declar01'),
    url(r'^declar02/(?P<idfoy>\d{1})/$', 'simulation.views.declar02'),
    url(r'^declar03/(?P<idfoy>\d{1})/$', 'simulation.views.declar03'),
    url(r'^declar04/(?P<idfoy>\d{1})/$', 'simulation.views.declar04'),
    url(r'^declar05/(?P<idfoy>\d{1})/$', 'simulation.views.declar05'), 
    url(r'^output/$', 'simulation.views.output', name='output'),
    url(r'^graph/$', 'simulation.views.graph', name='graph'),
    )  
