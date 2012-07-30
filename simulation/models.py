# -*-coding:Utf-8 -*

#from django.db import models
import datetime
from django.db import models

from django.forms import Form, ModelForm, IntegerField, DateField, ChoiceField, BooleanField, ValidationError  
from django.forms.formsets import BaseFormSet
from django import template

from django.forms.extras.widgets import SelectDateWidget

from django.forms.fields import CheckboxInput



QUIFOY = (('vous', 'Vous'), ('conj', 'Conjoint'), ('pac', 'Personne à charge'))
QUIFAM = (('parent_1', 'parent 1'), ('parent_2', 'parent 2'), ('enfant', 'enfant'))
SO = ((1, u"Accédant à la propriété"),
      (2, u"Propriétaire non accédant"), 
      (3, u"Locataire d'un logement HLM"),
      (4, u"Locataire ou sous-locataire d'un logement loué vide non-HLM"),
      (5, u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel"),
      (6, u"Logé gratuitement par des parents, des amis ou l'employeur"))
register = template.Library()

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

class IndividualForm(Form):
    noi = IntegerField(label = 'n°')
    birth   = DateField(widget = SelectDateWidget(years=range(1900, datetime.date.today().year)))
    idfoy  = IntegerField(label = 'Numéro de déclaration')
    quifoy  = ChoiceField(label = 'Position déclaration impôts',choices = QUIFOY)
    #remplirdeclar = BooleanField(required = False, initial = True, label = 'Foyer')
    idfam = IntegerField(label = 'Numéro de famille')
    quifam = ChoiceField(label = 'Position famille', choices = QUIFAM )


#class MenageForm(forms.Form):
#    def __init__(self, *args, **kwargs):
#        scenario = kwargs.pop('scenario')
#        super(MenageForm, self).__init__(*args, **kwargs)
#            for individual in 

class LogementForm(Form):
    so = ChoiceField(label = "Statut d'occupation",choices = SO)
    loyer = IntegerField(label = 'Loyer', initial = 500)
    code_postal = IntegerField(label = 'Code postal', initial = 69001)
#   zone_apl = IntegerField(label = 'Zone allocation logement', initial = 2)

#class Logement(QDialog, Ui_Logement):
#    def __init__(self, scenario, parent = None):
#        super(Logement, self).__init__(parent)
#        self.setupUi(self)
#        self.parent = parent
#        self.scenario = scenario
#        self.spinCP.setValue(scenario.menage[0]['code_postal'])
#        self.spinLoyer.setValue(scenario.menage[0]['loyer'])
#        self.comboSo.setCurrentIndex(scenario.menage[0]['so']-1)
#                        
#        code_file = open('data/code_apl', 'r')
#        code_dict = pickle.load(code_file)
#        code_file.close()
#
#        def update_ville(code):        
#            if str(code) in code_dict:
#                commune = code_dict[str(code)]
#                self.bbox.button(QDialogButtonBox.Ok).setEnabled(True)
#            else:
#                commune = ("Ce code postal n'est pas reconnu", '2')
#                self.bbox.button(QDialogButtonBox.Ok).setEnabled(False)
#                
#            self.commune.setText(commune[0])
#            self.spinZone.setValue(int(commune[1]))
#
#        update_ville(self.spinCP.value())
#
#        self.connect(self.spinCP, SIGNAL('valueChanged(int)'), update_ville)
#        
#        def so_changed(value):
#            if value in (0,1):
#                self.spinLoyer.setValue(0)
#                self.spinLoyer.setEnabled(False)
#            else:
#                self.spinLoyer.setValue(500)
#                self.spinLoyer.setEnabled(True)
#                
#        self.connect(self.comboSo, SIGNAL('currentIndexChanged(int)'), so_changed)
#        self.connect(self.bbox, SIGNAL("accepted()"), SLOT("accept()"))
#        self.connect(self.bbox, SIGNAL("rejected()"), SLOT("reject()"))
#        
#    def accept(self):
#        self.scenario.menage[0].update({'loyer': int(self.spinLoyer.value()),
#                                        'so': int(self.comboSo.currentIndex()+1),
#                                        'zone_apl': int(self.spinZone.value()),
#                                        'code_postal': int(self.spinCP.value())})
#        QDialog.accept(self)

