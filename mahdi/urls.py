from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'mahdi.views.index'),
    url(r'^home/$', 'mahdi.views.home', name='home'),
    url(r'^menage/$', 'mahdi.views.menage'),
    url(r'^logement/$', 'mahdi.views.logement'),
    url(r'^declar01/$', 'mahdi.views.declar01'),
    url(r'^declar02/$', 'mahdi.views.declar02'),
    url(r'^declar03/$', 'mahdi.views.declar03'),
    url(r'^declar04/$', 'mahdi.views.declar04'),
    url(r'^declar05/$', 'mahdi.views.declar05'), # TODO clean this decla0i
    url(r'^output/$', 'mahdi.views.output'),
    url(r'^graph.png$', 'mahdi.views.graph', name='graph'),)  