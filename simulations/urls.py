from django.conf.urls import patterns, url
#from django.views.generic import DetailView, ListView
#from simulations.models import SimulationForm

urlpatterns = patterns('',
    url(r'^nouvelle_simulation/$', 'simulations.views.simulation'),
    url(r'^resultats/$', 'simulations.views.simulation')
)