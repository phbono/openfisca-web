# -*-coding:Utf-8 -*

from django.http import HttpResponse
from django.shortcuts import render
from simulation.models import IndividualForm, LogementForm
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from simulation.lanceur import Simu, Compo, BaseScenarioFormSet
from django.template import RequestContext



def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")
# form = IndividualForm()
# return render_to_response('simulation/menage.html', {'formset': form})

def menage(request):
    compo = request.session.get('compo',default=None)
    if compo == None:
        compo = Compo()

    if request.method == 'POST':

        if 'reset' in request.POST:
            if 'compo' in request.session:
                del request.session['compo']
            compo = Compo()
            formset = compo.gen_formset()
            request.session['compo'] = compo

        else:
            ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet, extra=0)
            formset = ScenarioFormSet(request.POST)
            if formset.is_valid():
                compo.scenario = formset.get_scenario()
        
                if 'add' in request.POST:
                    compo.addPerson()
                    
                if 'remove' in request.POST:
                    compo.scenario.rmvIndiv(compo.scenario.nbIndiv()-1)

                formset = compo.gen_formset()
                request.session['compo'] = compo
                
                if 'submit' in request.POST:
                    compo.scenario.genNbEnf()
                    ok = True
                    ok = build_simu(compo.scenario)
                    print 'is it ok ? :', ok
                    #return (request, 'simulation/menage.html', {'formset' : formset})
            
    else:
        
        formset = compo.gen_formset()
        request.session['compo'] = compo

    return render(request, 'simulation/menage.html', {'formset' : formset})


def build_simu(scenario):
    simu = Simu(scenario=scenario)
    simu.set_date()
    msg = simu.scenario.check_consistency()
    if msg:
        print 'inconsistent scenario'
    simu.set_param()
    x = simu.compute()
    for child in x.children:
            for child2 in child.children:
                print child2.code
                print child2._vals
    return True

def logement(request):
    if request.method == 'POST':
        logeform = LogementForm(request.POST)
        if logeform.is_valid():
            logeform.cleaned_data
            return render_to_response('simulation/logement.html', {'logementform': logeform}, context_instance=RequestContext(request))
    else:
        logeform = LogementForm()
    c = {'logementform': logeform}
    c.update(csrf(request))
    return render_to_response('simulation/logement.html', c)




# for indinv in formset['noiindiv']