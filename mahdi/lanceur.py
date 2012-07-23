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

from core.utils import gen_output_data
from core.utils import Scenario
from parametres.paramData import XmlReader, Tree2Object
from Config import CONF
from france.data import InputTable
from france.model import ModelFrance
from core.datatable import DataTable, SystemSf

class Simu(object):
    def __init__(self, scenario=None, root_dir=None):
        super(Simu, self).__init__()

        self.set_config(directory=root_dir)

        
        self.set_scenario(scenario)
        self.scenario.genNbEnf()
        
        
    def set_config(self, directory = None, nmen=1):
        '''
        Sets the directory where to find the openfisca source and adjust some directories
        '''
        if directory == None:
#            dir = "C:/Users/Utilisateur/My Documents/Aptana Studio 3 Workspace/web/srcopen"
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
        data_courant = gen_output_data(population_courant)
        return data_courant


def main():
    simu = Simu()
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
    
    
    

if __name__=='__main__':
    main()