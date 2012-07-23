# -*-coding:Utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from simulation.models import IndividualForm
from django.forms.formsets import formset_factory, BaseFormSet
from datetime import datetime     
from core.utils import Scenario
from django.core.urlresolvers import reverse

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
    
    delete = False
    if delete: 
        del request.session['scenario']

    scenario = request.session.get('scenario',default=None)
    if scenario == None:
        print 'scenario is None'
        scenario = Scenario()

    if request.method == 'POST':    # ADD
        ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet, extra=0)
        formset = ScenarioFormSet(request.POST)
        for form in formset.cleaned_data:
            print form
        print formset.is_valid()
        if formset.is_valid():

            scenario = formset2scenario(formset)
            scenario.addIndiv(0, datetime(1975,1,1).date(), 'vous', 'chef')
            print scenario
            formset = scenario2formset(scenario)
            request.session['scenario'] = scenario        
            return render(request, 'simulation/menage.html', {'formset' : formset})

    else:
        
        formset = scenario2formset(scenario)
        request.session['scenario'] = scenario

    return render(request, 'simulation/menage.html', {'formset' : formset})


def formset2scenario(formset):
    scenario = Scenario()
    for form in formset.cleaned_data:
        scenario.addIndiv( form['noi'], form['birth'], form['quifoy'], form['quifam'])        
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