# -*-coding:Utf-8 -*

from simulations.models import IndividuForm
from facades import lanceur

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
    
    
    simu = lanceur.Simu()
    simu.set_openfica_root_dir()
    simu.set_date()
    msg = simu.scenario.check_consistency()
    if msg:
        print 'inconsistent scenario'
    simu.set_param()
    print simu.param_courant
    print simu.scenario
    
    x = simu.compute()
    dictionnaire = dict()
    for child in x.children:
            for child2 in child.children:
                dictionnaire[child2.code] = child2._vals
                print child2.code
                #print child2._vals
    #print('voici le dictionnaire')
    #print dictionnaire
    #for nombre in dictionnaire['rev_trav']:
    #    print nombre
    nombre = dictionnaire['rev_trav']
    nombre2 = nombre[5]
    print nombre2
    
    data = {'no': nobis, 'nodeclar': nodeclarbis, 'test': testbis, 'test2': test2bis, 'nofam': nofambis}
    formulairemodifie = IndividuForm(data)
    return formulairemodifie
