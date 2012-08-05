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
    # TODO: REMOVE THIS PART AND ADD TO MAINSTREAM OPENFISCA
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


# TODO: REMOVE THIS PART AND ADD TO MAINSTREAM OPENFISCA AS SUPPLEMENTARY METHOD TO OutNode

from core.utils import OutNode
from numpy import count_nonzero

class MyNode(OutNode):
    def __init__(self, code = '', desc='', shortname = '', vals = 0, color = (0,0,0), typevar = 0, parent = None, is_null = None):
        super(MyNode, self).__init__(code, desc, shortname = '', vals = 0, color = (0,0,0), typevar = 0, parent = None)
        self.is_null = is_null
        
    def init_from_OutNode(self, OutNode):
        '''
        Creates a MyNOde from an OutNode
        '''
        for attr in ['code', 'desc', 'shortname', 'vals', 'color', 'typevar']:
            setattr(self, attr, getattr(OutNode, attr))
        
        if OutNode.childCount != 0:
            for child in  OutNode.children:
                new_child = MyNode()
                new_child.init_from_OutNode(child)
                self.addChild(new_child)        
        
    
    def signal_null_children(self):
        '''
        Sets the is_null attributes to True or False
        '''
        if self.is_null is not None:
            return
        else:
            self.is_null = True
        
        if self.childCount() == 0:
            if count_nonzero(self.vals) > 0:
                self.is_null = False
                return
        
        else:
            for child in self.children:                
                if child.is_null is not None:
                    if child.is_null is False:
                        self.is_null = False
                else:
                    child.signal_null_children()
                    if child.is_null is False:
                        self.is_null = False

    def remove_null_children(self):
        '''
        Remove all is_null attributes from MyNode
        '''
        self.signal_null_children()
        children = self.children[:]
        for child in children:
            if child.is_null:
                self.children.remove(child)
            else:
                child.remove_null_children()
                    
        if self.is_null:
            self.parent.children.remove(self)

    def create_fields_dict(self):
        self.remove_null_children()
        fields = dict()
        
        if self.childCount() == 0:
            fields[self.code] = self.vals[0]
            return fields  
        
        elif self.childCount() > 0:
            for child in self.children:
                new_fields = child.create_fields_dict()
                fields.update(new_fields)
            return fields
        
