'''
Created on Aug 3, 2012

@author: Utilisateur
'''


from mahdi.lanceur import Simu
 
from core.utils import Scenario, OutNode
from numpy import nonzero, count_nonzero


class MyNode(OutNode):
    def __init__(self, code = '', desc='', shortname = '', vals = 0, color = (0,0,0), typevar = 0, parent = None, is_null = None):
        super(MyNode, self).__init__(code, desc, shortname = '', vals = 0, color = (0,0,0), typevar = 0, parent = None)
        self.is_null = is_null
        
    def init_from_OutNode(self, OutNode):
        for attr in ['code', 'desc', 'shortname', 'vals', 'color', 'typevar']:
            setattr(self, attr, getattr(OutNode, attr))
        
        if OutNode.childCount != 0:
            for child in  OutNode.children:
                new_child = MyNode()
                new_child.init_from_OutNode(child)
                self.addChild(new_child)        
        
    
    def build_null_childs(self):
        if self.childCount() != 0:
            for child in self.children:
                if child.is_null is None:
                    child.build_null_childs()
                if child.is_null is False:
                    self.is_null = False
                else:
                    self.is_null = True
        else:
#            print 'val', self.vals
#            print nonzero(self.vals)
#            print count_nonzero(self.vals)
            if count_nonzero(self.vals) == 0 :  # TODO fix this
                self.is_null = True
            else:
                self.is_null = False
            



scenario = Scenario()
simu = Simu()
simu.build()
print simu.data_courant.__class__

x = MyNode()
x.init_from_OutNode(simu.data_courant)


print simu.data_courant.vals
for child in x.children:
    for child2 in child.children:
        print child2.code, child2._vals,  child2.is_null

print 'x'
x.build_null_childs()
for child in x.children:
    for child2 in child.children:
        print child2.code, child2._vals,  child2.is_null

print x