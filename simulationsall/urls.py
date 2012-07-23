from django.conf.urls import patterns, url
#from django.views.generic import DetailView, ListView
from simulationsall.models import ChoixNombreIndividuForm

urlpatterns = patterns('',
    url(r'^choixnombreindividu/$', 'simulationsall.views.choixnombreindividu'),
#    url(r'^nouvelle_simulation/$', 'simulationsall.views.simulation', {'nombre_individu_rentre': args}),
    url(r'^resultats/$', 'simulationsall.views.simulation', {'nombre_individu_rentre': 1}),
)