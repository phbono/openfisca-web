# -*-coding:Utf-8 -*

from django.http import HttpResponse
from django.shortcuts import render
from mahdi.models import IndividualForm
from django.forms.formsets import formset_factory

from mahdi.lanceur import Simu, Compo, BaseScenarioFormSet




def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")
#    form = IndividualForm()
#    return render_to_response('mahdi/menage.html', {'formset': form})

def menage(request):

    compo = request.session.get('compo',default=None)
    if compo == None:
        compo = Compo()

    if request.method == 'POST':

        if 'reset' in request.POST:
            del request.session['compo']
            compo = Compo()
            formset = compo.gen_formset()
            request.session['compo'] = compo

        else:
            ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet, extra=0)
            formset = ScenarioFormSet(request.POST)
            
#            for form in formset.cleaned_data:
#                print form
            if formset.is_valid():
                scenario = formset.get_scenario()
        
                if 'add' in request.POST:
                    #compo.scenario.addIndiv(scenario.nbIndiv(), datetime(1975,1,1).date(), 'vous', 'chef')
                    print scenario
                    print 'add'
                    compo.addPerson()
                    
                if 'remove' in request.POST:
                    compo.scenario.rmvIndiv(scenario.nbIndiv()-1)
                        
#                print scenario
                formset = compo.gen_formset()
                request.session['compo'] = compo
                
                if 'submit' in request.POST:
                    compo.scenario.genNbEnf()
                    ok = True
                    ok = build_simu(compo.scenario)
                    print 'is it ok ? :', ok
                    #return (request, 'mahdi/menage.html', {'formset' : formset})    
            
    else:
        
        formset = compo.gen_formset()
        request.session['compo'] = compo

    return render(request, 'mahdi/menage.html', {'formset' : formset})



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







#    for indinv in formset['noiindiv']