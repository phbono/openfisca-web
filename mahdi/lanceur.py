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

from mahdi.models import IndividualForm, Declar1Form, Declar3Form 
from mahdi.utils import extract_foy_indiv, foy2of_dict, field2quifoy


class BaseScenarioFormSet(BaseFormSet):    
    def get_scenario(self):
        scenario = Scenario()
        for form in self.cleaned_data:
            noi, birth = form['noi']-1, form['birth']
            idfoy, quifoy, idfam, quifam = form['idfoy']-1, form['quifoy'], form['idfam']-1, form['quifam']
            scenario.indiv.update({noi:{'birth':birth, 
                                'inv'     : 0,
                                'alt'     : 0,
                                'activite': 0,
                                'quifoy'  : quifoy,
                                'quifam'  : quifam,
                                'noidec'  : idfoy,
                                'noichef' : idfam,
                                'noipref' : 0,
                                'statmarit': 2}})
            
            scenario._assignPerson(noi, quifoy = quifoy, foyer = idfoy, quifam = quifam, famille = idfam)
            scenario.updateMen()
        return scenario


class Simu(object):
    def __init__(self, scenario=None, root_dir=None):
        super(Simu, self).__init__()

        self.set_config(directory=root_dir)        
        self.set_scenario(scenario)
        #self.scenario.genNbEnf()
        
        
    def set_config(self, directory = None, nmen=101):
        '''
        Sets the directory where to find the openfisca source and adjust some directories
        '''
        if directory == None:
#   TODO REMOVE         dir = "C:/Users/Utilisateur/My Documents/Aptana Studio 3 Workspace/web/srcopen"
#            dir = "/home/florent/workspace/openfisca/srcopen/"
            cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
            predirectory = os.path.dirname(cmd_folder)
            directory = os.path.join(predirectory,'srcopen')

        CONF.set('paths', 'data_dir', os.path.join(directory,'data'))
        CONF.set('simulation', 'nmen', nmen)

         
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
        xaxis = 'sal' #self.xaxis
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
        if noi == 1: self.scenario.addIndiv(noi, birth = date(1975,1,1), quifoy = 'conj', quifam = 'part')
        else:        self.scenario.addIndiv(noi, birth = date(2000,1,1), quifoy = 'pac' , quifam = 'enf')

    def rmvPerson(self, noi = None):
        pass

    def gen_formset(self):
        
        scenario = self.scenario
        print self.scenario
        scenario_var_list = ['noi', 'birth', 'idfoy', 'quifoy', 'idfam', 'quifam', 'statmarit', 'activite']
        
        convert = dict(idfoy = "noidec", idfam ="noichef")
        zero_start = [ "idfoy", "idfam", "noi"]

        ScenarioFormSet = formset_factory(IndividualForm, formset = BaseScenarioFormSet)
        
        data = {'form-TOTAL_FORMS': scenario.nbIndiv(),
                'form-INITIAL_FORMS': scenario.nbIndiv(),
                'form-MAX_NUM_FORMS': u'',}
        
        for noi, indiv in scenario.indiv.iteritems():
            for var in scenario_var_list:
                if var == "noi":
                    data['form-' + str(noi)+'-' + str(var)] = noi
                elif var == "quifoy" and indiv[var][:3] == "pac":
                    data['form-' + str(noi)+'-' + str(var)] = "pac"
                elif var == "quifam" and indiv[var][:3] == "enf":
                    data['form-' + str(noi)+'-' + str(var)] = "enf"
                elif var in convert.keys():
                    data['form-' + str(noi)+'-' + str(var)] = indiv[convert[var]]
                else:
                    data['form-' + str(noi)+'-' + str(var)] = indiv[var]       
                if var in zero_start:
                    data['form-' + str(noi)+'-' + str(var)] += 1
                

        formset = ScenarioFormSet(data=data)
        

        return formset



    def create_declar1(self, idfoy = None):
        '''
        Creates a Declar1Form from compo.scenario data
        '''
        if idfoy is None:
            idfoy = 0
        
        data = dict(statmarit=2)
        for indiv in self.scenario.indiv.itervalues():
            if indiv['noidec'] == idfoy:            
                data[indiv['quifoy']] = indiv['birth']
                if indiv['quifoy'] == 'vous':
                    data['statmarit'] = int(1)
        
        form = Declar1Form(data)

        for name, field in form.fields.iteritems():
            if name in data.keys():
                field.required = True
            else:
                field.required = False
        return form
    
    def create_declar3(self, idfoy = None, description=None):
        '''
        Creates a Declar3Form from compo.scenario data
        '''
        if idfoy is None:
            idfoy = 0
            
        if description is None:
            print 'a description should be provided' # TODO convert this to exception
            
        declar = self.scenario.declar[idfoy]
        cleaned_indiv = extract_foy_indiv(self.scenario, idfoy=idfoy)
        data = declar
        
        def indiv2foy(varname, quifoy):
            '''
            Yields the field of the foy corresponding to the varname 
            '''
            convert = foy2of_dict()
            
            value = None
            for field in convert.keys():
                if field2quifoy(field) == quifoy:    
                    if convert[field] == varname:
                        value = field
            return value
            
        for person in cleaned_indiv.itervalues():
            for varname, value in person.iteritems():
                quifoy = person['quifoy']
                field = indiv2foy(varname, quifoy)
                data[field]  = value
            
        form = Declar3Form(data=declar, description=description)
        return form        

            
    def create_declar(self, formClass, idfoy = None):
        '''
        Creates a Declar?Forms from compo.scenario data
        Works for Declar2Form, Declar4Form, Declar5Form 
        
        '''
        if idfoy is None:
            idfoy = 0
            
        declar = self.scenario.declar[idfoy]
        form = formClass(data=declar)
        return form
    

    def set_logement(self, values):
        '''
        Sets logement values in scenario
        '''
        loyer = values['loyer']
        so = values['so']
        zone_apl = values['zone_apl']
        code_postal = values['code_postal']
        self.scenario.menage[0].update({'loyer': int(loyer),
                                        'so': int(so),
                                        'zone_apl': int(zone_apl),
                                        'code_postal': int(code_postal)})

    def get_declar1(self, data = None, idfoy = 0):
        '''
        Sets declar1 values in compo.scenario  from a Delcar1Form
        '''

        statmarit = data['statmarit']
        
        for indiv in self.scenario.indiv.itervalues(): 
            if indiv['noidec'] == idfoy:
                if indiv['quifoy'] in ['vous', 'conj']:
                    indiv['statmarit'] = statmarit
                indiv['birth'] = data[indiv['quifoy']]

    def get_declar(self, form = None, idfoy = 0):
        '''
        Gets declar values in compo.scenario from DeclarForms
        Works for Declar2Form, Declar4Form, Declar5Form 
        
        '''
        declar = self.scenario.declar[idfoy]
        data = form.cleaned_data
        
        for field, value in data.iteritems(): 
            declar[field] = value

    def get_declar3(self, form = None, idfoy = 0):
        '''
        Gets declar values in compo.scenario from Declar3Form
        '''
        declar = self.scenario.declar[idfoy]

        # Build a dict of individulas present on the declar
        cleaned_indiv = extract_foy_indiv(self.scenario, idfoy= idfoy)

        convert = foy2of_dict()
                        
        data = form.cleaned_data
        
        for field, value in data.iteritems(): 
            if field in convert.keys():
                quifoy  = field2quifoy(field)
                varname = convert[field]
                for person in cleaned_indiv.itervalues():
                    if person['quifoy'] == quifoy:
                        person[varname] = value
            else:
                declar[field] = value


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
        
    return commune[0], commune[1]    


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