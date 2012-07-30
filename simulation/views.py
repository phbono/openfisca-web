# -*-coding:Utf-8 -*

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from simulation.models import IndividualForm, LogementForm
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from simulation.lanceur import Simu, Compo, BaseScenarioFormSet
from django.template import RequestContext
from lanceur import get_zone


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
                    simu = build_simu(compo.scenario)                    
                    request.session['simu'] = simu
                    print 'fin de la soumission'
                    return HttpResponseRedirect('simulation/output/')  
            
    else:
        
        formset = compo.gen_formset()
        request.session['compo'] = compo
    c = {'formset': formset}
    c.update(csrf(request))
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

#def logement(request):
#    if request.method == 'POST':
#        logementform = LogementForm(request.POST)
#        if logementform.is_valid():
#            logementform.cleaned_data
#            return render_to_response('simulation/logement.html', {'logementform': logementform}, context_instance=RequestContext(request))
#    else:
#        logementform = LogementForm()
#    c = {'logementform': logementform}
#    c.update(csrf(request))
#    return render_to_response('simulation/logement.html', c)

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
    else:
        logt_form = LogementForm()
    c = {'logt_form': logt_form}
    c.update(csrf(request))
    return render(request, 'simulation/logement.html', c)

#def logement(request):
#    
#    logementform = request.session.get('logementform',default=None)
#    
#    if logementform == None:
#        logementform = LogementForm()
#    request.session['logementform'] = logementform
#    if request.method == 'POST':
#
#        logementform = LogementForm(request.POST)
#        if logementform.is_valid():
#            logementform.cleaned_data
#            request.session['logementform'] = logementform
#     
#    return render(request, 'simulation/logement.html', {'logementform' : logementform})

def output(request):
    print 'entrée dans output'
    return render_to_response('simulation/output.html')

def graph(request):
    simu = request.session['simu']
    simu.build_graph()
    canvas = simu.canvas
    response= HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response



def home(request):
    return render_to_response('simulation/home.html')

# for indinv in formset['noiindiv']