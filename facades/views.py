# -*-coding:Utf-8 -*

from simulations.models import IndividuForm
#from srcopen.lanceur import Simu, main

def facade(formulairerempli):
    
    nobis = formulairerempli['no'].value()
    nobis = int(nobis)
    
    nodeclarbis = formulairerempli['nodeclar'].value()
    nodeclarbis = int(nodeclarbis)
    
    testbis = formulairerempli['test'].value()
    testbis = int(testbis)
    
    test2bis = formulairerempli['test2'].value()
    test2bis = int(test2bis)
    
    nofambis = formulairerempli['nofam'].value()
    nofambis = int(nofambis)
    
    data = {'no': nobis, 'nodeclar': nodeclarbis, 'test': testbis, 'test2': test2bis, 'nofam': nofambis}
    formulairemodifie = IndividuForm(data)
    return formulairemodifie
