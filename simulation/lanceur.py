# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, inspect
from datetime import date

from django.forms.formsets import formset_factory, BaseFormSet

from core.utils import gen_output_data
from core.utils import Scenario
from widgets.Output import drawBareme
from parametres.paramData import XmlReader, Tree2Object
from Config import CONF
from france.data import InputTable
from france.model import ModelFrance
from core.datatable import DataTable, SystemSf

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from simulation.models import IndividualForm

class BaseScenarioFormSet(BaseFormSet):
#    def clean(self):
#        """Checks consistency of a formset"""
#        if any(self.errors):
#            # Don't bother validating the formset unless each form is valid on its own
#            return
    
    def get_scenario(self):
        scenario = Scenario()
        for form in self.cleaned_data:
            noi, birth = form['noi']-1, form['birth']
            idfoy, quifoy, idfam, quifam = form['idfoy']-1, form['quifoy'], form['idfam']-1, form['quifam']
            scenario.addIndiv(noi, birth, quifoy, quifam)
            scenario._assignPerson(noi, quifoy = quifoy, foyer = idfoy, quifam = quifam, famille = idfam)
            
        return scenario


class Simu(object):
    def __init__(self, scenario=None, root_dir=None):
        super(Simu, self).__init__()

        self.set_config(directory=root_dir)        
        self.set_scenario(scenario)
        #self.scenario.genNbEnf()
        
        
    def set_config(self, directory = None, nmen=1):
        '''
        Sets the directory where to find the openfisca source and adjust some directories
        '''
        if directory == None:
#   TODO REMOVE         dir = "C:/Users/Utilisateur/My Documents/Aptana Studio 3 Workspace/web/srcopen"
#            dir = "/home/florent/workspace/openfisca/srcopen/"
            cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
            predirectory = os.path.dirname(cmd_folder)
            directory = os.path.join(predirectory,'srcopen')

        CONF.set('paths', 'data_dir',os.path.join(directory,'data'))
        CONF.set('simulation', 'nmen',1)

         
    def set_scenario(self, scenario=None):
        if scenario is None:
            self.scenario = Scenario()
        else:
            self.scenario = scenario  
        
    def set_date(self, date=None):
        if date == None:
            self._date = CONF.get('simulation', 'datesim')
        else:
            self._date = date
            CONF.set('simulation', 'datesim',str(self._date))
        print self._date
        
    def set_param(self):
        '''
        Sets the parameters of the simulation
        '''
        data_dir = CONF.get('paths', 'data_dir')
        fname = os.path.join(data_dir, 'param.xml')
        reader = XmlReader(fname, self._date)
        rootNode = reader.tree
        
        self.param_default = Tree2Object(rootNode, defaut=True)
        self.param_default.datesim = self._date

        self.param_courant = Tree2Object(rootNode, defaut=False)
        self.param_courant.datesim = self._date
                
    def compute(self):
        '''
        Computes the totals  
        '''
        input_table = DataTable(InputTable, scenario = self.scenario)
        population_courant = SystemSf(ModelFrance, self.param_courant, self.param_default)
        population_courant.set_inputs(input_table)
        self.data_courant = gen_output_data(population_courant)


    def set_xaxis(self):
        temp = {u'Salaire super brut': 'salsuperbrut',
        u'Salaire brut' : 'salbrut',
        u'Salaire imposable': 'sal',
        u'Salaire net': 'salnet',
        u'Chômage brut' : 'chobrut',
        u'Chômage imposable': 'cho',
        u'Chômage net': 'chonet',
        u'Retraite brut': 'rstbrut',
        u'Retraite imposable' : 'rst',
        u'Retraite nette': 'rstnet'}
        if self.mode == "bareme":
            self.xaxis = temp[unicode(self.absBox.currentText())]
        
    def set_mode(self, mode):
        '''
        Sets graph mode (bareme/waterfall)
        '''
        self.mode = mode 

    def build_graph(self):
        '''
        Builds graph
        '''
        data = self.data_courant
        xaxis = self.xaxis
        reforme = False
        dataDefault = None
        legend = True
        fig=Figure()
        ax=fig.add_subplot(111)
        drawBareme(data, ax, xaxis, reforme = reforme,
                    dataDefault = dataDefault, legend = legend)
        canvas = FigureCanvas(fig)
        self.canvas = canvas
#        response= HttpResponse(content_type='image/png')
#        canvas.print_png(response)
#        return response



class Compo(object):
    def __init__(self):
        super(Compo, self).__init__()
        self.scenario = Scenario()
        

    def nbRow(self):
        return self.scenario.nbIndiv()

    def addPerson(self):
        
        noi = self.nbRow()
        print noi
        if noi == 1: self.scenario.addIndiv(noi, birth = date(1975,1,1), quifoy = 'conj', quifam = 'part')
        else:        self.scenario.addIndiv(noi, birth = date(2000,1,1), quifoy = 'pac' , quifam = 'enf')
        print 'scenario at the end of addPerson'
        print self.scenario

    def rmvPerson(self, noi = None):
        pass

    def gen_formset(self):
        
        scenario = self.scenario
        print 'scenario at the beginning of gen_formset'
        print scenario
        scenario_var_list = ['noi', 'birth', 'idfoy', 'quifoy', 'idfam', 'quifam']
        
        convert = dict(idfoy = "noidec", idfam ="noichef")
        zero_start = [ "idfoy", "idfam", "noi"]
        initial = []    
    
        for noi, indiv in scenario.indiv.iteritems():
            new_form = {}
            for var in scenario_var_list:
                if var == "noi":
                    new_form[var] = noi
                elif var in convert.keys():
                    new_form[var] = indiv[convert[var]]
                else:
                    new_form[var] = indiv[var]       
                if var in zero_start:
                    new_form[var] += 1
            
            print 'new_form for noi: ' + str(noi)        
            print new_form        
            initial.append(new_form)
            
            
        ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet, extra=0)
        
        formset = ScenarioFormSet(initial=initial)
        
        print formset.is_valid()
        if True: #formset.is_valid():
            for form in formset.forms:
                print form.is_valid()
                if form.is_valid():
                    print form.cleaned_data
        return formset


    def set_logement(self, values):
        '''
        Sets logement values in scenario
        '''
        loyer = values['loyer']
        so = values['so']
        #zone_apl = values['zone_apl']
        code_postal = values['code_postal']
        self.scenario.menage[0].update({'loyer': int(loyer),
                                        'so': int(so),
                                        #'zone_apl': int(zone_apl),
                                        'code_postal': int(code_postal)})

    


# TODO move this to main openfisca branch
import pickle

def get_zone(postal_code):
    '''
    Takes the postal_code as input argument
    Returns a list with the name of the commune and the apl zone  
    '''
    # TODO: REMOVE THIS PART
    cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    predirectory = os.path.dirname(cmd_folder)
    directory = os.path.join(predirectory,'srcopen')
    
    code = postal_code
    code_file = open(os.path.join(directory,'data/code_apl'), 'r')
    code_dict = pickle.load(code_file)
    code_file.close()

    if str(code) in code_dict:
        commune = code_dict[str(code)]
    else:
        commune = ("Ce code postal n'est pas reconnu", '2')
        
    return commune    


def main():
    simu = Simu()
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
    
    
    

if __name__=='__main__':
    main()