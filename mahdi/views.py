# -*-coding:Utf-8 -*

from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from mahdi.models import (IndividualForm,
                          LogementForm,
                          Declar1Form, Declar2Form, Declar3Form, Declar4Form, Declar5Form)

from django.forms.formsets import formset_factory
from mahdi.lanceur import Simu, Compo, BaseScenarioFormSet
from france.data import InputTable
from core.datatable import DataTable
from django.template import RequestContext

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")
#    form = IndividualForm()
#    return render_to_response('mahdi/menage.html', {'formset': form})

def menage(request):
    compo = request.session.get('compo', default=None)
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
                    simu = build_simu(compo.scenario)                    
                    request.session['simu'] = simu
                    print 'fin de la soumission'
                    return HttpResponseRedirect('mahdi/output/')
#                    return render_to_response('mahdi/output.html')    
            
    else:
        
        formset = compo.gen_formset()
        request.session['compo'] = compo

    c = {'formset': formset}
    c.update(csrf(request))
    return render(request, 'mahdi/menage.html', c)


from lanceur import get_zone

def logement(request):

    print 'entering logement'
    print request.method
    compo = request.session.get('compo', default=None)
    
    if request.method == 'POST':
        logt_form = LogementForm(request.POST)
        if logt_form.is_valid():
            vals = logt_form.cleaned_data
            print request.POST    
            if 'submit' in request.POST:
                print 'logement submit'
                code_postal = vals['code_postal']
                commune = get_zone(code_postal)
                print 'commune :  ', commune[0]
                print 'zone :  '   , commune[1]    

                
                compo.set_logement(vals)
                
                
                print compo.scenario
            elif 'reset' in request.POST:
                print 'reset'
            elif 'validate' in request.POST:
                print 'logement validate' 
                
    
#    if request.method == 'GET':
#        logt_form = LogementForm(request.GET)
#        if logt_form.is_valid():
#            if 'validate' in request.GET:
#                print 'logement validate' 
#                postal_code = vals['postal_code']
#                commune = get_zone(postal_code)
#                print 'commune :  ', commune[0]
#                print 'zone :  '   , commune[1]
#            elif 'reset' in request.GET:
#                print 'reset'
            
#            return render_to_response('mahdi/logement.html', {'logementform': logt_form}, context_instance=RequestContext(request))
    else:
        logt_form = LogementForm()
    c = {'logt_form': logt_form}
    c.update(csrf(request))
    return render(request, 'mahdi/logement.html', c)

#    return render_to_response('mahdi/logement.html', {'logementform': logt_form}, context_instance=RequestContext(request))
    
#    return render_to_response('mahdi/logement.html', c)




def output(request):
    print 'entrée dans output'
    return render_to_response('mahdi/output.html')

def graph(request):
    simu = request.session['simu']
    simu.build_graph()
    canvas = simu.canvas
    response= HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response



def home(request):
    return render_to_response('mahdi/home.html')

def declar01(request):
    compo = request.session.get('compo' , default=None)
    print compo.scenario
    form = Declar1Form()
    idfoy = 0
    form.set_declar(compo=compo , idfoy=idfoy)

#    print form.is_valid()
#    if form.is_valid():
#        print form.cleaned_data

    if request.method == 'POST':
        print 'is the form valid :', form.is_valid()
        
#        if True:    
        if form.is_valid():

            # TODO do things
            request.session.modified = True
            return HttpResponseRedirect('/mahdi/declar02/')

    
        else:
            print 'is bound :', form.is_bound
            for field in form:
                if field._errors: 
                    print field.name
                    print field._errors
                    
                
    return render(request, 'mahdi/declar01.html', {'form' : form})   
        

def declar02(request):
    form = Declar2Form()
        
    if request.method == 'POST':
        if True:
#        if form.is_valid():
            request.session.modified = True
            return HttpResponseRedirect('/mahdi/declar03/')
    else:
        form = Declar2Form() 

    return render(request, 'mahdi/declar02.html', {'form' : form})   
    
    
def declar03(request):
    description = DataTable(InputTable).description
    form = Declar3Form(description = description)
        
    if request.method == 'POST':
        if True:
#        if form.is_valid():
            request.session.modified = True
            return HttpResponseRedirect('/mahdi/declar04/')
    else:
        form = Declar3Form(description = description) 

    return render(request, 'mahdi/declar03.html', {'form' : form})

def declar04(request):
    form = Declar4Form()
        
    if request.method == 'POST':
        if True:
#        if form.is_valid():
            request.session.modified = True
            return HttpResponseRedirect('/mahdi/declar05/')
    else:
        form = Declar4Form() 

    return render(request, 'mahdi/declar04.html', {'form' : form})

def declar05(request):
    form = Declar5Form()
        
    if request.method == 'POST':
        if True:
#        if form.is_valid():
            request.session.modified = True
            # lancer les calculs
    else:
        form = Declar5Form() 

    return render(request, 'mahdi/declar05.html', {'form' : form})




# MOVE this to somewhere else !
def build_simu(scenario):
    simu = Simu(scenario=scenario)
    simu.set_date()
    msg = simu.scenario.check_consistency()
    if msg:
        print 'inconsistent scenario'
    simu.set_param()
    simu.compute()
#    simu.build_graph()
#    
#    
#    for child in x.children:
#            for child2 in child.children:
#                print child2.code
#                print child2._vals
    return simu






#    for indinv in formset['noiindiv']