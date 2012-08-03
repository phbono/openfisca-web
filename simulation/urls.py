from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'simulation.views.index'),
    url(r'^home/$', 'simulation.views.home', name='home'),
    url(r'^menage/$', 'simulation.views.menage'),
    url(r'^logement/$', 'simulation.views.logement'),
    url(r'^declar01/$', 'simulation.views.declar01'),
    url(r'^declar02/$', 'simulation.views.declar02'),
    url(r'^declar03/$', 'simulation.views.declar03'),
    url(r'^declar04/$', 'simulation.views.declar04'),
    url(r'^declar05/$', 'simulation.views.declar05'), # TODO clean this decla0i
    url(r'^output/$', 'simulation.views.output'),
    url(r'^graph.png$', 'simulation.views.graph', name='graph'),
    url(r'^graphtest$', 'simulation.views.graphtest'),
    url(r'^graphtest2$', 'simulation.views.graphtest2'),
    url(r'^graphtest3$', 'simulation.views.graphtest3'),)