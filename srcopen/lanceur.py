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

from datetime import datetime

from core.utils import Scenario, gen_output_data
from parametres.paramData import XmlReader, Tree2Object

from france.data import InputTable
from france.model import ModelFrance
from core.datatable import DataTable, SystemSf
import sys

class Simu(object):
    def __init__(self):
        super(Simu, self).__init__()

        self.set_scenario()
        self.scenario.genNbEnf()
        
    def set_scenario(self):
        self.scenario = Scenario()
        
    def set_date(self, date):
        self._date = datetime.strptime(date ,"%Y-%m-%d").date()
        
        
    def set_param(self, fname = None):
        '''
        '''
        if fname == None:
            fname='/home/florent/workspace/openfisca/srcopen/data/param.xml'
        
        reader = XmlReader(fname, self._date)
        rootNode = reader.tree
        
        self.param_default = Tree2Object(rootNode, defaut=True)
        self.param_default.datesim = self._date

        self.param_courant = Tree2Object(rootNode, defaut=False)
        self.param_courant.datesim = self._date
                
    def compute(self):
        input_table = DataTable(InputTable, scenario = self.scenario)
        population_courant = SystemSf(ModelFrance, self.param_courant, self.param_default)
        population_courant.set_inputs(input_table)
        data_courant = gen_output_data(population_courant)
        self.results = data_courant
        return data_courant


def main():
    simu = Simu()
    simu.set_date("2010-01-01")
    msg1 = simu.scenario.check_consistency()
    if msg1:
        print 'inconsistent scenario'
    simu.set_param()
    print simu.param_courant
    print simu.scenario
    
    x = simu.compute()
    for child in x.children:
            for child2 in child.children:
                print child2.code
                print child2._vals
    

if __name__=='__main__':
    sys.exit(main())