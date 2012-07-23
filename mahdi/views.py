# -*-coding:Utf-8 -*

from django.http import HttpResponse
from django.shortcuts import render
from mahdi.models import IndividualForm
from django.forms.formsets import formset_factory, BaseFormSet
from datetime import datetime     
from core.utils import Scenario
from mahdi.lanceur import Simu


class BaseScenarioFormSet(BaseFormSet):
    def clean(self):
        """Checks consistency of a formset"""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return


def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")
#    form = IndividualForm()
#    return render_to_response('mahdi/menage.html', {'formset': form})

def menage(request):
    
    scenario = request.session.get('scenario',default=None)
    if scenario == None:
        print 'scenario is None'
        scenario = Scenario()

    if request.method == 'POST':

        if 'reset' in request.POST:
            del request.session['scenario']
            scenario = Scenario()
            formset = scenario2formset(scenario)
            request.session['scenario'] = scenario

        else:
            ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet, extra=0)
            formset = ScenarioFormSet(request.POST)
            
#            for form in formset.cleaned_data:
#                print form
            if formset.is_valid():
                scenario = formset2scenario(formset)
        
                if 'add' in request.POST:
                    scenario.addIndiv(scenario.nbIndiv(), datetime(1975,1,1).date(), 'vous', 'chef')
                if 'remove' in request.POST:
                    scenario.rmvIndiv(scenario.nbIndiv()-1)
                        
#                print scenario
                formset = scenario2formset(scenario)
                request.session['scenario'] = scenario
                
                if 'submit' in request.POST:
                    scenario.genNbEnf()
                    ok = True
                    ok = build_simu(scenario)
                    print 'is it ok ? :', ok
                    #return (request, 'mahdi/menage.html', {'formset' : formset})    
            
    else:
        
        formset = scenario2formset(scenario)
        request.session['scenario'] = scenario

    return render(request, 'mahdi/menage.html', {'formset' : formset})



def build_simu(scenario):
    simu = Simu(scenario=scenario)
    simu.set_openfica_root_dir()
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

def formset2scenario(formset):
    scenario = Scenario()
    for form in formset.cleaned_data:
        noi, birth, quifoy, quifam = form['noi']-1, form['birth'], form['quifoy'], form['quifam']
        scenario.addIndiv(noi, birth, quifoy, quifam)
    return scenario


def scenario2formset(scenario):
    var_list = ['noi', 'birth', 'idfoy', 'quifoy', 'idfam', 'quifam']
    
    convert = dict(idfoy = "noidec", idfam ="noichef")
    zero_start = [ "idfoy", "idfam", "noi"]
    initial = []    

    for noi, indiv in scenario.indiv.iteritems():
        new_form = {}
        for var in var_list:
            if var == "noi":
                new_form[var] = noi
            elif var in convert.keys():
                new_form[var] = indiv[convert[var]]
            else:
                new_form[var] = indiv[var]       
            if var in zero_start:
                new_form[var] += 1
                
        initial.append(new_form)
        
    ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet, extra=0)
    return ScenarioFormSet(initial=initial)



#    for indinv in formset['noiindiv']