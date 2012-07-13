from simulations.models import IndividuForm

def facade(formulairerempli):
    variable_1bis = formulairerempli['variable_1'].value() # recuperation de la valeur de la variable 1
    variable_1bis = int(variable_1bis) # reconversion sous forme d'entier
    variable_1bis += 1 # modification de la variable
    variable_2bis = formulairerempli['variable_2'].value()
    variable_3bis = formulairerempli['variable_3'].value()
    data = {'variable_1': variable_1bis, 'variable_2': variable_2bis, 'variable_3': variable_3bis}
    formulairemodifie = IndividuForm(data)
    return formulairemodifie
