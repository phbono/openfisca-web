# -*-coding:Utf-8 -*

#from django.db import models
import datetime
from django.db import models

from django.forms import Form, IntegerField, DateField, ChoiceField, BooleanField, TextInput  

from django import template

from django.forms.extras.widgets import SelectDateWidget

from django.forms.fields import CheckboxInput



pacs   = [ ('pac' + str(i), 'Personne à charge')  for i in range(1,10)]
QUIFOY = (('vous', 'Vous'), ('conj', 'Conjoint')) +  tuple(pacs)
enfants = [ ('enf' + str(i), 'enfant')  for i in range(1,10)]
QUIFAM = (('chef', 'parent 1'), ('part', 'parent 2')) + tuple(enfants) 

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



#class DeclarForm(Form):
#    def __init__(self, *args, **kwargs):
#        extra = kwargs.pop('extra')
#        super(Form, self).__init__(*args, **kwargs)
#
#        for code, label in extra:
#            
#            self.fields[code] = CharField(label=label)


class MyBooleanField(BooleanField):
    def __init__(self, *args, **kwargs):
        BooleanField.__init__(self, required=False, *args, **kwargs)


class MyIntegerField(IntegerField):
#    def __init__(self, kwargs = {}, *args):
    def __init__(self, *args, **kwargs):
        widgetAttr = {'size':'8', 
                      'align': 'right',
                      'maxlength':'9', 
                      'style' : "text-align: right"
                      }
        wid = TextInput(attrs=widgetAttr)
        fieldAttr = {'max_value': 999999999, 
                     'min_value': 0,
                     'required' : False,
                     'localize': True
                     }
        fieldAttr.update(kwargs)
        IntegerField.__init__(self, widget = wid, **fieldAttr)


class MyDateField(DateField):
    def __init__(self, kwargs = {}):
        wid = SelectDateWidget(years = [i for i in reversed(xrange(1900,2010))])
        fieldAttr = {'required' : False, 
                     'localize': True
                     }
        fieldAttr.update(kwargs)
        DateField.__init__(self, widget= wid, **fieldAttr)



class Declar1Form(Form):
    statmarit = ChoiceField(choices = ((2,'Célibataire'), (1,'Marié'), (5,'Pacsé'), (4,'Veuf'),(5,'Divorcé')))
    
    def __init__(self, *args, **kwargs):
        #extra = kwargs.pop('extra')
        super(Declar1Form, self).__init__(*args, **kwargs)

        birth_dates = ['birthv','birthc'] + ['birth' + str(i) for i in range(1,10)]
        for birth_date in birth_dates:
            if birth_date == 'birthv':
                self.fields[birth_date] = MyDateField({'required':True})
            else:
                self.fields[birth_date] = MyDateField()



class Declar2Form(Form):
    def __init__(self, *args, **kwargs):
        #extra = kwargs.pop('extra')
        super(Declar2Form, self).__init__(*args, **kwargs)

        cases = ['caseL', 'caseE', 'caseN', 'caseP', 'caseF', 'caseW', 'caseS', 'caseG', 'caseT']  
        for case in cases:
            self.fields[case] = MyBooleanField()
            

from core.columns import BoolCol, IntCol

class Declar3Form(Form):
    def __init__(self, *args, **kwargs):
        description = kwargs.pop('description')
        print description.col_names
        super(Declar3Form, self).__init__(*args, **kwargs)
        fields = ['sali', 'choi', 'fra', 'cho_ld', 'hsup', 'ppe_tp_sa',
                   'ppe_du_sa',  'f1bl', 'f1cb', 'f1dq', 
                   'rsti', 'f1at', 'alr']
        for field in fields:
            
            print 'is ' + str(field) + ' in description :' + str( field in description.col_names) 
            
            if field not in ['f1bl', 'f1cb', 'f1dq', 'f1dq', 'f1at']:
                col = description.get_col(field)
                if col.label is not None:
                    label = col.label
                else:
                    label = field    
                print col
                print label
                
                if isinstance(col, IntCol):
                    self.fields[field] = MyIntegerField(label=label)
                if isinstance(col, BoolCol):
                    self.fields[field] = MyBooleanField(label=label)

#    f1aj = MyIntegerField()
#    f1ap = MyIntegerField()
#    f1ak = MyIntegerField()
#    f1ai = MyBooleanField() cho_ld

#    f1au = MyIntegerField() hsup
#    f1ax = MyBooleanField()
#    f1av = MyIntegerField()

#    f1bl = MyIntegerField()
#    f1cb = MyIntegerField()
#    f1dq = MyIntegerField()

#    f1as = MyIntegerField() rsti
#    f1ao = MyIntegerField() alr

    

#class IndividuForm(forms.Form):
#    def 
#    __init__(self, indiv = None):
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



