# -*-coding:Utf-8 -*

#from django.db import models
from django import forms, template
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
from django.forms.fields import CheckboxInput

POSITION_DECLARATION_CHOICES = (('vous', 'Vous'), ('conj', 'Conjoint'), ('pac', 'Personne à charge'))
POSITION_FAMILLE_CHOICES = (('parent_1', 'parent 1'), ('parent_2', 'parent 2'), ('enfant', 'enfant'))

register = template.Library()

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

class ChoixNombreIndividuForm(forms.Form):
    nombre_individu = forms.IntegerField(label = "Nombre d'individu", initial = 1, help_text = '10 individus maximum.')

class IndividuForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    no = forms.IntegerField(label = 'n°', initial = 1)
    date_de_naissance = forms.DateField(widget = SelectDateWidget(), initial = timezone.now())
    nodeclar = forms.IntegerField(label = 'Numéro de déclaration', initial = 1)
    positiondeclar = forms.ChoiceField(label = 'Position déclaration impôts',choices = POSITION_DECLARATION_CHOICES)
    remplirdeclar = forms.BooleanField(required = False, initial = True, label = 'Foyer')
#    test = forms.IntegerField(label = 'foyer1', initial = 42)
#    test2 = forms.IntegerField(label = 'foyer2', initial = 42)
    nofam = forms.IntegerField(label = 'Numéro de famille', initial = 1)
    positionfam = forms.ChoiceField(label = 'Position déclaration impôts',choices = POSITION_FAMILLE_CHOICES)



#    def __init__(self, *args, **kwargs):                        #fonction pour rajouter un paramètre au formulaire
#        no = kwargs.pop('no')
#        super(SimulationForm, self).__init__(*args, **kwargs)
#        self.fields = forms.IntegerField(label = 'n°')