# -*-coding:Utf-8 -*

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from mahdi.models import IndividualForm, Declar1Form, Declar2Form, Declar3Form
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
                    #return (request, 'mahdi/menage.html', {'formset' : formset})    
            
    else:
        
        formset = compo.gen_formset()
        request.session['compo'] = compo

    return render(request, 'mahdi/menage.html', {'formset' : formset})


def home(request):
    return render_to_response('mahdi/home.html')

def declar01(request):

    form = Declar1Form() 
#    print form.is_valid()
#    if form.is_valid():
#        print form.cleaned_data

    if request.method == 'POST':
#        if form.is_valid():
        print 'POST'
    else:
        form = Declar1Form() 

    return render(request, 'mahdi/declar01.html', {'form' : form})   
        

def declar02(request):
    form = Declar2Form()
        
    if request.method == 'POST':
#        if form.is_valid():
        print 'POST'
    else:
        form = Declar1Form() 

    return render(request, 'mahdi/declar02.html', {'form' : form})   
    
from france.data import InputTable
from core.datatable import DataTable
    
def declar03(request):
    form = Declar3Form(description= DataTable(InputTable).description)
        
    if request.method == 'POST':
#        if form.is_valid():
        print 'POST'
    else:
        form = Declar1Form() 

    return render(request, 'mahdi/declar03.html', {'form' : form})


def declar04(request):
    form = Declar2Form()
        
    if request.method == 'POST':
#        if form.is_valid():
        print 'POST'
    else:
        form = Declar1Form() 

    return render(request, 'mahdi/declar04.html', {'form' : form})


# MOVE this to somewhere else !
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