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
from core.utils import Scenario


def extract_foy_indiv(scenario = None, idfoy = None):
    '''
    Build a dict of individuals present on the declar
    '''
    # TODO write warnings/exceptions
    if scenario == None:
        scenario = Scenario()
    if idfoy == None:
        idfoy = 0    
    
    indiv = scenario.indiv
    cleaned_indiv = dict()
    for person in indiv:
        if indiv[person]['noidec'] == idfoy:
            cleaned_indiv[person] = indiv[person]
    return cleaned_indiv
    
def foy2of_dict():
    '''
    Produces a convenient dict for conversion from fields in delacr3 to var in opefisca
    '''
    convert = dict()
    abcd = ['a', 'b', 'c', 'd']
    for l in abcd: 
        convert['f1'+l+'j' ] = 'sali'
        convert['f1'+l+'p' ] = 'choi'
        convert['f1'+l+'k' ] = 'fra'
        convert['f1'+l+'i' ] = 'cho_ld'
        convert['f1'+l+'u' ] = 'hsup'
        convert['f1'+l+'x' ] = 'ppe_tp_sa'
        convert['f1'+l+'v' ] = 'ppe_du_sa'
        convert['f1'+l+'s' ] = 'rsti'
        convert['f1'+l+'o' ] = 'alr'             
    return convert

def field2quifoy(field):
    '''
    Extracts quifoy from field in declar3
    '''
    letter2quifoy = {'a': 'vous', 'b': 'conj', 'c': 'pac1', 'd': 'pac2', 'e': 'pac3'}
    return letter2quifoy[field[2]]
    
        
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


