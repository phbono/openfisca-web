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
QUIFAM = (('chef', 'parent 1'), ('part', 'parent 2'), ('enf', 'enfant'))

register = template.Library()

@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)

#class Individual(models.Model):
#    noindiv = models.IntegerField(label = 'n°', initial = 1)
#    birth   = models.DateField(widget = SelectDateWidget(), initial = timezone.now())
#    noidec  = models.IntegerField(label = 'Numéro de déclaration', initial = 1)
#    quifoy  = models.CharField(label = 'Position déclaration impôts',choices = QUIFOY)
#    remplirdeclar = models.BooleanField(required = False, initial = True, label = 'Foyer')
#    noifam = models.IntegerField(label = 'Numéro de famille', initial = 1)
#    quifam = models.CharField(label = 'Position déclaration impôts',choices = QUIFAM)
#        
#    def __unicode__(self):
#        return self.noindiv
#    
#class IndividualForm(ModelForm):
#    class Meta:
#        model = Individual


class IndividualForm(Form):
    noi = IntegerField(label = 'n°')
    birth   = DateField(widget = SelectDateWidget(years=range(1900, datetime.date.today().year)))
    idfoy  = IntegerField(label = 'Numéro de déclaration')
    quifoy  = ChoiceField(label = 'Position déclaration impôts',choices = QUIFOY)
    #remplirdeclar = BooleanField(required = False, initial = True, label = 'Foyer')
    idfam = IntegerField(label = 'Numéro de famille')
    quifam = ChoiceField(label = 'Position famille', choices = QUIFAM )




#class IndividuForm(forms.Form):
#    def __init__(self, indiv = None):
#        super(IndividuForm, self).__init__()
#    # indiv est un dict de dict. La clé est le noi de l'individu
#    # Exemple :
#    # 0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0, 
#    #     'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0}
#        if indiv == None:
#            indiv = {0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0,
#                         'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0} 


#class MenageForm(forms.Form):
#    def __init__(self, *args, **kwargs):
#        scenario = kwargs.pop('scenario')
#        super(MenageForm, self).__init__(*args, **kwargs)
#            for individual in 



