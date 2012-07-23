# -*-coding:Utf-8 -*

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from simulationsall.models import IndividuForm, ChoixNombreIndividuForm
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from facades.views import facade
from django.forms.formsets import formset_factory
from django.template import RequestContext
    
#------un seul individu------
    
#def simulation(request):
#    if request.method == 'POST': # If the form has been submitted...
#        indivform = IndividuForm(request.POST) # A form bound to the POST data
#        if indivform.is_valid(): # All validation rules pass
#            indivform.cleaned_data
#            #indivform = facade(indivform)
#            #return HttpResponseRedirect(reverse('simulations.views.resultats', form)) # Redirect after POST
#            return render_to_response('simulations/resultats.html', {'individuform': indivform})
#    else:
#        indivform = IndividuForm() # An unbound form
#    c = {'individuform': indivform}
#    c.update(csrf(request))
#    return render_to_response('simulations/simulation.html', c)


#------plusieurs individus------

#IndividuFormSet = formset_factory(IndividuForm, extra = 3)
#data = {
#        'form-TOTAL_FORMS': u'2',
#        'form-INITIAL_FORMS': u'2',
#        'form-MAX_NUM_FORMS': u'10',
#        }
##indivform = IndividuFormSet(data)


def choixnombreindividu(request):
    if request.method == 'POST':
        choixnombreindividuform = ChoixNombreIndividuForm(request.POST)
        if choixnombreindividuform.is_valid(): 
            choixnombreindividuform.cleaned_data
            #return render_to_response('simulationsall/nouvelle_simulation.html', {'choixnombreindividuform': choixnombreindividuform,}, context_instance=RequestContext(request))
            return HttpResponseRedirect(reverse('simulationsall.views.simulation', args=(choixnombreindividuform['nombre_individu'].value(),)))
    else:
        choixnombreindividuform = ChoixNombreIndividuForm()
    c = {'choixnombreindividuform': choixnombreindividuform}
    c.update(csrf(request))
    return render_to_response('simulationsall/choixnombreindividu.html', c)

def simulation(request, nombre_individu_rentre):
    IndividuFormSet = formset_factory(IndividuForm, extra = nombre_individu_rentre)
    data = {
        'form-TOTAL_FORMS': nombre_individu_rentre,
        'form-INITIAL_FORMS': u'2',
        'form-MAX_NUM_FORMS': u'10',
        }
    if request.method == 'POST':
        formset = IndividuFormSet(data, request.POST)
        if formset.is_valid():
            formset.cleaned_data
            #indivform = facade(indivform)
            return HttpResponseRedirect(reverse('simulationsall.views.resultats', {'formset': formset}))
            #return render_to_response('simulationsall/resultats.html', {'formset': formset})
    else:
        formset = IndividuFormSet(data)
    c = {'formset': formset}
    c.update(csrf(request))
    return render_to_response('simulationsall/simulation.html', c)

def resultats(request, simulationform):
    return render_to_response('simulationsall/resultats.html', {'simulationform': simulationform})