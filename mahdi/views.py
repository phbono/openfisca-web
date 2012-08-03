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


def menage(request):
    compo = request.session.get('compo', default=None)
    if compo == None:
        compo = Compo()
    if compo.scenario.nbIndiv() == 0:
        compo = Compo()

    if request.method == 'POST':

        if 'reset' in request.POST:
            if 'compo' in request.session:
                del request.session['compo']
            compo = Compo()
            formset = compo.gen_formset()
            request.session['compo'] = compo

        else:
            ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet)
            formset = ScenarioFormSet(request.POST)
            if formset.is_valid():
                compo.scenario = formset.get_scenario()
        
                if 'add' in request.POST:
                    compo.addPerson()
                    
                elif 'remove' in request.POST:
                    compo.scenario.rmvIndiv(compo.scenario.nbIndiv()-1)

                elif 'validate' in request.POST:
                    print compo.scenario
                
                formset = compo.gen_formset()
                request.session['compo'] = compo
                
                if 'submit' in request.POST:
                    compo.scenario.genNbEnf()

                    simu = build_simu(compo.scenario)                    
#                    for child in simu.data_courant.children:
#                        for child2 in child.children:
#                            print child2.code
#                            print child2._vals
#    
                    request.session['data'] = simu.data_courant
                    return render(request, 'mahdi/output.html')
            else:
                print 'fromset is not vali in menage' 
            
    else:
        
        formset = compo.gen_formset()
        request.session['compo'] = compo

    units = {'foy': range(1,len(compo.scenario.declar)+1),
             'fam': range(1,len(compo.scenario.famille)+1),
             'ind': range(1,compo.scenario.nbIndiv()+1)}
    
    c = {'formset': formset, 'units' : units}
    c.update(csrf(request))
    return render(request, 'mahdi/menage.html', c)

def output(request):
    return render_to_response('mahdi/output.html')    


from matplotlib.figure import Figure
from widgets.Output import drawBareme, drawWaterfall
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def graph_old(request):
    data = request.session['data']
#    for child in data.children:
#        for child2 in child.children:
#            print child2.code
#            print child2._vals

    
    xaxis = 'sal' #self.xaxis
    reforme = False
    dataDefault = None
    legend = False
    fig = Figure()
    ax = fig.add_subplot(111)
    drawWaterfall(data, ax)
#    drawBareme(data, ax, xaxis, reforme = reforme,
#               dataDefault = dataDefault, legend = legend)
#    drawBareme(ax, data)
#    print 'apres drawbareme'
#    print fig

    canvas = FigureCanvas(fig)    
    response= HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response



from chartit import DataPool, Chart
def graph(request):
    data = request.session['data']
        
    

    weatherdata = DataPool(
           series=
            [{'options': {
                'source': MonthlyWeatherByCity.objects.all()},
              'terms': [
                'month',
                'houston_temp', 
                'boston_temp']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = openfisca_data,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'month': [
                    'boston_temp',
                    'houston_temp']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Openfisca'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})


from lanceur import get_zone

def logement(request):

    print 'entering logement'
    print request.method
    compo = request.session.get('compo', default=None)
    commune = 'Indéterminée'
    zone_apl = None
    
    if request.method == 'POST':
        logt_form = LogementForm(request.POST)
        if logt_form.is_valid():
            vals = logt_form.cleaned_data
            print request.POST    
            if 'submit' in request.POST:
                print 'logement submit'
                code_postal = vals['code_postal']
                commune, zone_apl = get_zone(code_postal)
                compo.set_logement(vals)
                
                print compo.scenario
            elif 'reset' in request.POST:
                print 'reset'
            elif 'validate' in request.POST:
                print 'logement validate' 
                
    else:
        logt_form = LogementForm()
    c = {'logt_form': logt_form, 'commune' : commune, 'zone_apl' :zone_apl}
    c.update(csrf(request))
    return render(request, 'mahdi/logement.html', c)


def home(request):
    return render_to_response('mahdi/home.html')    

def declar01(request, idfoy=None):
    compo = request.session.get('compo' , default=None)
    if idfoy is None:
        idfoy = 0
    else:
        idfoy = int(idfoy)     
    
    if request.method == 'POST':
        form = Declar1Form(request.POST)
        if form.is_valid():
            compo.get_declar1(data=form.cleaned_data, idfoy = idfoy)
            form = compo.create_declar1(idfoy=idfoy)        
            request.session['compo'] = compo
            return HttpResponseRedirect('/mahdi/declar02/' + str(idfoy))

    else:
        form  = compo.create_declar1(idfoy=idfoy)
    
    request.session['compo'] = compo            
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'mahdi/declar01.html', c)   
        

def declar02(request, idfoy):
    compo = request.session.get('compo' , default=None)
    if idfoy is None:
        idfoy = 0
    else:
        idfoy = int(idfoy)     

    if request.method == 'POST':
        print 'entering POST'
        form = Declar2Form(request.POST)
        if form.is_valid():
            compo.get_declar(form=form, idfoy = idfoy)
            form = compo.create_declar(Declar2Form, idfoy=idfoy)        
            request.session['compo'] = compo
            return HttpResponseRedirect('/mahdi/declar03/' + str(idfoy))        

    else:
        form  = compo.create_declar(Declar2Form, idfoy=idfoy)

    request.session['compo'] = compo            
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'mahdi/declar02.html', c)   
    
    
def declar03(request, idfoy):
    
    description = DataTable(InputTable).description
    compo = request.session.get('compo' , default=None)
    if idfoy is None:
        idfoy = 0
    else:
        idfoy = int(idfoy)     
    
    if request.method == 'POST':
        form = Declar3Form(request.POST, description = description)
        print 'declar 3: is form valid :', form.is_valid() 
        if form.is_valid():
            compo.get_declar3(form=form, idfoy = idfoy)
            form = compo.create_declar3(idfoy=idfoy, description = description)        
            request.session['compo'] = compo
            for indiv, val in compo.scenario.indiv.iteritems():
                print indiv
                print val
                
            return HttpResponseRedirect('/mahdi/declar04/' + str(idfoy))

    else:
    
        form = Declar3Form(description = description)

    request.session['compo'] = compo            
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'mahdi/declar03.html', c)   

        

def declar04(request, idfoy):
    compo = request.session.get('compo' , default=None)
    if idfoy is None:
        idfoy = 0
    else:
        idfoy = int(idfoy)     

    if request.method == 'POST':
        print 'entering POST'
        form = Declar4Form(request.POST)
        if form.is_valid():
            compo.get_declar(form=form, idfoy = idfoy)
            form = compo.create_declar(Declar4Form, idfoy=idfoy)        
            request.session['compo'] = compo
            return HttpResponseRedirect('/mahdi/declar05/' + str(idfoy))

    else:
        form  = compo.create_declar(Declar4Form, idfoy=idfoy)

    request.session['compo'] = compo
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'mahdi/declar04.html', c)   


def declar05(request, idfoy = None):
    compo = request.session.get('compo' , default=None)
    if idfoy is None:
        idfoy = 0
    else:
        idfoy=int(idfoy)
    
    if request.method == 'POST':
        form = Declar5Form(request.POST)
        if form.is_valid():
            compo.get_declar(form=form, idfoy = idfoy)
            form = compo.create_declar(Declar5Form, idfoy=idfoy)        
            request.session['compo'] = compo
            return render(request, 'mahdi/menage.html')
    else:
        form  = compo.create_declar(Declar5Form, idfoy=idfoy)

    request.session['compo'] = compo            
    c = {'form': form}
    c.update(csrf(request))
    return render(request, 'mahdi/declar05.html', c)   




#import numpy as np
#import pylab
#from matplotlib.patches import PathPatch
#
#def drawBareme(ax1, data):
#    n = len(data)
#    MAXREV = 50000
#    NMEN = 101
#    XAXIS = 'sal'
#    MODE = 'bareme'
#    xdata = np.linspace(0, MAXREV, NMEN)
#
#    ax1.hold(True)
#
#    # On trace le revenu disponible
#    ax1.plot(xdata, data.revdisp.vals, color = data.revdisp.color, linewidth = 3, zorder = 51)
#    p = [pylab.Line2D([0,1],[.5,.5],color = data.revdisp.color)]
#    l = [data.revdisp.desc]
#
#    prv = np.zeros(NMEN)
#    for serie in data.getNonNuls():
#        cur = serie.cumu
#        col = serie.color
#        dsc = serie.desc
#        cod = serie.code
#
#        if cod != 'irpp':
#            a = ax1.fill_between(xdata, prv , cur, color = col, linewidth = 0.5, edgecolor = 'black', picker = True )
#            a.set_label(dsc)
#            p.insert(0,pylab.Rectangle((0, 0), 1, 1, fc = col, linewidth = 0.5, edgecolor = 'black' ))
#            l.insert(0,dsc)
#        elif cod == 'irpp':
#            imp = ax1.fill_between(xdata, cur, prv, linewidth = 2, edgecolor = 'blue', zorder = 50, picker = True )
#            imp.set_label(dsc)                
#            imp.set_facecolors("none")
#
#            for path in imp.get_paths():
#                patch = PathPatch(path, fc="none", hatch="\\")
#                ax1.add_patch(patch)
#                patch.set_zorder(49)
#
#            p.insert(0,pylab.Rectangle((0, 0), 1, 1, fc=(1,1,1,0), edgecolor = 'blue', hatch = '\\'))
#            l.insert(0,dsc)
#        prv = cur
#    
#            
#    if   XAXIS == 'sal': xlabel = u'Salaires de la personne de référence'
#    elif XAXIS == 'cho': xlabel = u'Allocation chômage de la personne de référence'
#    elif XAXIS == 'rst': xlabel = u'Pensions de retraite de la personne de référence'
#    ax1.set_xlabel(xlabel)
#    ax1.set_ylabel(u"Revenu disponible")
#    ax1.set_xlim(0, np.amax(xdata))
#    if   MODE == 'bareme' : ax1.set_ylim(0, np.amax(xdata))
#    elif MODE == 'reforme': ax1.set_ylim(auto = True)
#
#    ax1.legend(p,l,loc= 4, prop = {'size':'medium'})

